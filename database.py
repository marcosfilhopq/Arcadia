import sqlite3  # Biblioteca padrão para interação com bancos SQLite

# Inicializa o banco de dados e cria a tabela de usuários
def init_db():
    conn = sqlite3.connect('users.db')  # Conecta ao banco de dados (cria se não existir)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # ID único para cada usuário
            username TEXT UNIQUE NOT NULL,        # Nome de usuário único
            password TEXT NOT NULL,               # Senha do usuário
            is_admin INTEGER DEFAULT 0           # Indica se o usuário é admin (0 = não, 1 = sim)
        )
    ''')
    conn.commit()  # Salva as alterações
    conn.close()   # Fecha a conexão

# Adiciona um novo usuário ao banco de dados
def add_user(username, password, is_admin=0):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)',
                       (username, password, is_admin))
        conn.commit()  # Salva o novo usuário
    except sqlite3.IntegrityError:
        return False  # Retorna False se o usuário já existir
    finally:
        conn.close()  # Fecha a conexão
    return True  # Usuário adicionado com sucesso

# Recupera informações de um usuário pelo nome de usuário
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password, is_admin FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()  # Retorna (senha, is_admin) ou None
    conn.close()
    return user

# Atualiza informações de um usuário existente
def update_user(username, new_username=None, new_password=None):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    if new_username:
        cursor.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, username))
    if new_password:
        cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()  # Salva as alterações
    conn.close()   # Fecha a conexão