import pytest  # Biblioteca para testes automatizados
import sqlite3  # Biblioteca para interação com banco SQLite
from database import init_db, add_user, get_user, update_user  # Funções do banco a serem testadas

# Fixture para configurar e limpar o banco antes dos testes
@pytest.fixture
def client():
    init_db()  # Inicializa o banco de dados
    clear_db()  # Limpa a tabela antes de cada teste

# Função para limpar a tabela de usuários
def clear_db():
    conn = sqlite3.connect('users.db')  # Conecta ao banco de dados
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users')  # Remove todos os usuários
    conn.commit()
    conn.close()

# Teste para adição de usuários
def test_add_user(client):
    # Verifica se um usuário pode ser adicionado
    result = add_user('testuser', 'testpass')
    assert result is True  # Usuário deve ser adicionado com sucesso

    # Verifica se não é possível adicionar o mesmo usuário novamente
    result = add_user('testuser', 'testpass')
    assert result is False  # Deve retornar False para usuário duplicado

# Teste para recuperação de usuários
def test_get_user(client):
    # Adiciona um usuário para testar a recuperação
    add_user('testuser', 'testpass')
    user = get_user('testuser')

    # Verifica se o usuário foi encontrado
    assert user is not None
    assert user[0] == 'testpass'  # Confirma a senha correta
    assert user[1] == 0  # Confirma que não é admin

# Teste para atualização de usuários
def test_update_user(client):
    # Adiciona um usuário e testa a atualização
    add_user('testuser', 'testpass')
    update_user('testuser', new_username='newuser', new_password='newpass')

    # Recupera o usuário atualizado e verifica os novos dados
    user = get_user('newuser')
    assert user is not None
    assert user[0] == 'newpass'  # Confirma a nova senha
