import unittest  # Biblioteca padrão para criação de testes
from app import app, db, User  # Importa o aplicativo, banco de dados e modelo de usuário

class AppTestCase(unittest.TestCase):
    # Configuração inicial antes de cada teste
    def setUp(self):
        self.app = app.test_client()  # Cria um cliente de teste para simular requisições
        self.app.testing = True  # Ativa o modo de teste
        db.create_all()  # Cria as tabelas no banco de dados para os testes

    # Limpeza após cada teste
    def tearDown(self):
        db.session.remove()  # Remove a sessão do banco de dados
        db.drop_all()  # Apaga todas as tabelas para um ambiente limpo

    # Teste para verificar a criação de um usuário
    def test_user_creation(self):
        user = User(username='testuser', password='testpass')  # Cria um novo usuário
        db.session.add(user)  # Adiciona o usuário ao banco
        db.session.commit()  # Salva as alterações
        # Verifica se o usuário foi criado com sucesso
        self.assertIsNotNone(User.query.filter_by(username='testuser').first())

    # Teste para verificar o login de um usuário
    def test_login(self):
        # Cria um usuário para teste de login
        user = User(username='testuser', password='testpass')
        db.session.add(user)
        db.session.commit()

        # Realiza uma requisição POST para a rota de login
        response = self.app.post('/login', data=dict(username='testuser', password='testpass'))
        # Verifica se o redirecionamento ocorreu após login (código 302)
        self.assertEqual(response.status_code, 302)

    # Teste para verificar o registro de um novo usuário
    def test_register(self):
        # Realiza uma requisição POST para a rota de registro
        response = self.app.post('/register', data=dict(username='newuser', password='newpass'))
        # Verifica se o redirecionamento ocorreu após registro (código 302)
        self.assertEqual(response.status_code, 302)

# Executa os testes se o script for rodado diretamente
if __name__ == '__main__':
    unittest.main()