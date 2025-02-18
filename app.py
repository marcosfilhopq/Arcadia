from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import subprocess 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seu_banco_de_dados.db'  # Ajuste conforme necessário
app.secret_key = 'sua_chave_secreta'  # Troque por uma chave secreta real
db = SQLAlchemy(app)

# Definição do modelo User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Campo para verificar se é admin

# Inicializa o banco de dados
@app.before_first_request
def create_tables():
    db.create_all()
    # Adiciona um usuário administrador inicial (apenas para teste)
    if not User.query.filter_by(username='admin').first():  # Verifica se o usuário já existe
        admin_user = User(username='admin', password='admin123', is_admin=True)
        db.session.add(admin_user)
        db.session.commit()

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redireciona para a página de login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # user.password é a senha
            session['username'] = username
            session['is_admin'] = user.is_admin  # user.is_admin é o status de admin
            flash('Acesso aceito!')  # Mensagem de sucesso
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard
        else:
            flash('Usuário ou senha inválidos!')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')  # Renderiza o dashboard
    else:
        return redirect(url_for('login'))  # Redireciona para o login se não estiver autenticado

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password and user.is_admin:  # Verifica se é admin
            session['username'] = username
            session['is_admin'] = user.is_admin  # user.is_admin é o status de admin
            flash('Acesso ao painel administrativo aceito!')  # Mensagem de sucesso
            return redirect(url_for('admin'))  # Redireciona para o painel de administração
        else:
            flash('Usuário ou senha inválidos ou não é um administrador!')
    
    return render_template('admin_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not User.query.filter_by(username=username).first():  # Verifica se o usuário já existe
            new_user = User(username=username, password=password, is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            flash('Registro realizado com sucesso! Você pode fazer login agora.')
            return redirect(url_for('login'))
        else:
            flash('Usuário já existe! Escolha outro.')
    
    return render_template('register.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session or not session.get('is_admin'):
        flash('Acesso negado!')
        return redirect(url_for('admin_login'))  # Redireciona para a página de login do admin

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
            flash('Erro ao atualizar o usuário. Verifique se o usuário existe.')

    # Consulta para obter usuários não administradores
    non_admin_users = User.query.filter_by(is_admin=False).all()  # Obtém todos os usuários que não são administradores
    return render_template('admin.html', users=non_admin_users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Usuário excluído com sucesso!', 'success')
    else:
        flash('Usuário não encontrado!', 'error')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('Você foi desconectado.')
    return redirect(url_for('login'))

@app.route('/start_minesweeper')
def start_minesweeper():
    subprocess.Popen(["python", "minesweeper_app.py"])
    return "O jogo foi iniciado em uma nova janela!"

if __name__ == '__main__':
    app.run(debug=True)