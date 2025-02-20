from flask import Flask, render_template, request, redirect, url_for, session, flash  # Importa módulos do Flask
from flask_sqlalchemy import SQLAlchemy  # Integração com banco de dados SQLite
from flask_socketio import SocketIO, emit  # Comunicação em tempo real
import subprocess  # Executa jogos externos
from games.tic_tac_toe_game import start_tic_tac_toe  # Função para iniciar o Jogo da Velha
import threading  # Executa suporte em paralelo
import time  # Utilizado para delays se necessário

# Inicializa o app Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seu_banco_de_dados.db'  # Configuração do banco de dados SQLite
app.secret_key = 'sua_chave_secreta'  # Chave secreta para sessões

# Inicializa banco de dados e SocketIO
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Modelo de usuário para o banco de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID do usuário
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nome de usuário
    password = db.Column(db.String(120), nullable=False)  # Senha do usuário
    is_admin = db.Column(db.Boolean, default=False)  # Flag para administrador

# Cria tabelas e usuário admin padrão
@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(username='admin').first():  # Verifica se admin existe
        admin_user = User(username='admin', password='admin123', is_admin=True)
        db.session.add(admin_user)
        db.session.commit()

# Rota inicial redireciona para página home
@app.route('/')
def home():
    return redirect(url_for('home_page'))

# Página Home
@app.route('/home')
def home_page():
    return render_template('home.html')

# Login de usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            session['is_admin'] = user.is_admin
            flash('Acesso aceito!')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos!')
    return render_template('login.html')

# Dashboard principal
@app.route('/arcadia')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

# Login do Administrador
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password and user.is_admin:
            session['username'] = username
            session['is_admin'] = user.is_admin
            flash('Acesso ao painel administrativo aceito!')
            return redirect(url_for('admin'))
        else:
            flash('Usuário ou senha inválidos ou não é um administrador!')
    return render_template('admin_login.html')

# Cadastro de novos usuários
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(username=username).first():
            new_user = User(username=username, password=password, is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            flash('Registro realizado com sucesso!')
            return redirect(url_for('login'))
        else:
            flash('Usuário já existe!')
    return render_template('register.html')

# Painel administrativo para gerenciar usuários
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session or not session.get('is_admin'):
        flash('Acesso negado!')
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        username = request.form['username']
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        user_to_update = User.query.filter_by(username=username).first()
        if user_to_update:
            user_to_update.username = new_username if new_username else user_to_update.username
            user_to_update.password = new_password if new_password else user_to_update.password
            db.session.commit()
            flash('Usuário atualizado com sucesso!')
        else:
            flash('Erro ao atualizar o usuário.')
    non_admin_users = User.query.filter_by(is_admin=False).all()
    return render_template('admin.html', users=non_admin_users)

# Deletar usuário
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Usuário excluído com sucesso!')
    else:
        flash('Usuário não encontrado!')
    return redirect(url_for('admin'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('Você foi desconectado.')
    return redirect(url_for('login'))

# Inicia o jogo Campo Minado
@app.route('/start_minesweeper')
def start_minesweeper():
    subprocess.Popen(["python", "games/minesweeper_app.py"])
    return "O jogo foi iniciado em uma nova janela!"

# Inicia o Jogo da Velha
@app.route('/jogodavelha')
def start_tic_tac_toe_route():
    start_tic_tac_toe()
    return "Jogo da Velha iniciado!"

# Inicia Pedra, Papel e Tesoura
@app.route('/ppt')
def start_ppt_route():
    subprocess.Popen(["python", "games/ppt.py"])
    return "O jogo foi iniciado em uma nova janela!"

# Inicia o jogo da Cobrinha
@app.route('/cobrinha')
def start_cobrinha_route():
    subprocess.Popen(["python", "games/cobrinha/main.py"])
    return "O jogo foi iniciado em uma nova janela!"

# Página de Chat
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Gerencia mensagens do Chat
@socketio.on('message')
def handle_message(data):
    print(f"Usuário: {data['data'].strip()}")
    emit('response', {'data': f'Usuário: {data["data"].strip()}'})

# Suporte envia mensagens pelo terminal
def run_support():
    while True:
        response = input("Suporte:\n")
        if response.strip():
            socketio.emit('response', {'data': f'Suporte: {response.strip()}'} )
            socketio.sleep(0)

# Executa a aplicação
if __name__ == '__main__':
    support_thread = threading.Thread(target=run_support, daemon=True)  # Inicia suporte em thread separada
    support_thread.start()
    socketio.run(app, debug=True)  # Executa servidor com debug ativo