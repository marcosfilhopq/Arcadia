import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, is_admin=0):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, password, is_admin))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Usuário já existe
    finally:
        conn.close()
    return True

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password, is_admin FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user  # Retorna (senha, is_admin) ou None

def update_user(username, new_username=None, new_password=None):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    if new_username:
        cursor.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, username))
    if new_password:
        cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()
    conn.close()