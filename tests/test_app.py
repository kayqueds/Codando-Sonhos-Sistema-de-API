import pytest
from src.app import create_app
from src.models import db
from src.models.user import User
from src.models.movie import Movie


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key-with-at-least-32-bytes-for-security',
    })

    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_and_login(client):
    payload = {'name': 'Henrique', 'email': 'henrique@example.com', 'password': 'Senha1234'}
    response = client.post('/auth/register', json=payload)
    assert response.status_code == 201
    assert response.json['user']['email'] == 'henrique@example.com'

    response = client.post('/auth/login', json={'email': 'henrique@example.com', 'password': 'Senha1234'})
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_list_users_requires_authentication(client):
    response = client.get('/users')
    assert response.status_code == 401


def test_user_update_and_access_control(client):
    payload = {'name': 'Maria', 'email': 'maria@example.com', 'password': 'Senha1234'}
    register = client.post('/auth/register', json=payload)
    token = client.post('/auth/login', json={'email': 'maria@example.com', 'password': 'Senha1234'}).json['access_token']
    user_id = register.json['user']['id']

    response = client.put(f'/users/{user_id}', json={'name': 'Maria Silva'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['user']['name'] == 'Maria Silva'

    response = client.put('/users/999', json={'name': 'Outro'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403


def test_delete_user(client):
    payload = {'name': 'Joao', 'email': 'joao@example.com', 'password': 'Senha1234'}
    register = client.post('/auth/register', json=payload)
    token = client.post('/auth/login', json={'email': 'joao@example.com', 'password': 'Senha1234'}).json['access_token']
    user_id = register.json['user']['id']

    response = client.delete(f'/users/{user_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Usuário excluído com sucesso.'

    response = client.post('/auth/login', json={'email': 'joao@example.com', 'password': 'Senha1234'})
    assert response.status_code == 401


def test_create_and_list_movies(client):
    # Registrar e logar usuário
    payload = {'name': 'Ana', 'email': 'ana@example.com', 'password': 'Senha1234'}
    client.post('/auth/register', json=payload)
    login = client.post('/auth/login', json={'email': 'ana@example.com', 'password': 'Senha1234'})
    token = login.json['access_token']

    # Criar filme
    movie_data = {'title': 'Inception', 'description': 'Filme de ficção científica'}
    response = client.post('/movies', json=movie_data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.json['movie']['title'] == 'Inception'

    # Listar filmes
    response = client.get('/movies', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.json['movies']) == 1


def test_get_update_delete_movie(client):
    # Registrar e logar usuário
    payload = {'name': 'Carlos', 'email': 'carlos@example.com', 'password': 'Senha1234'}
    register = client.post('/auth/register', json=payload)
    login = client.post('/auth/login', json={'email': 'carlos@example.com', 'password': 'Senha1234'})
    token = login.json['access_token']

    # Criar filme
    movie_data = {'title': 'The Matrix', 'description': 'Filme de ação'}
    create = client.post('/movies', json=movie_data, headers={'Authorization': f'Bearer {token}'})
    movie_id = create.json['movie']['id']

    # Obter filme
    response = client.get(f'/movies/{movie_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['movie']['title'] == 'The Matrix'

    # Atualizar filme
    update_data = {'title': 'The Matrix Reloaded', 'description': 'Sequência'}
    response = client.put(f'/movies/{movie_id}', json=update_data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['movie']['title'] == 'The Matrix Reloaded'

    # Deletar filme
    response = client.delete(f'/movies/{movie_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Filme excluído com sucesso.'

    # Verificar se foi deletado
    response = client.get(f'/movies/{movie_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404


def test_movie_access_control(client):
    # Dois usuários
    payload1 = {'name': 'User1', 'email': 'user1@example.com', 'password': 'Senha1234'}
    payload2 = {'name': 'User2', 'email': 'user2@example.com', 'password': 'Senha1234'}
    client.post('/auth/register', json=payload1)
    client.post('/auth/register', json=payload2)

    login1 = client.post('/auth/login', json={'email': 'user1@example.com', 'password': 'Senha1234'})
    login2 = client.post('/auth/login', json={'email': 'user2@example.com', 'password': 'Senha1234'})
    token1 = login1.json['access_token']
    token2 = login2.json['access_token']

    # User1 cria filme
    movie_data = {'title': 'Filme Privado'}
    create = client.post('/movies', json=movie_data, headers={'Authorization': f'Bearer {token1}'})
    movie_id = create.json['movie']['id']

    # User2 tenta acessar
    response = client.get(f'/movies/{movie_id}', headers={'Authorization': f'Bearer {token2}'})
    assert response.status_code == 404  # Não encontrado para outro usuário

    # User2 tenta atualizar
    response = client.put(f'/movies/{movie_id}', json={'title': 'Tentativa'}, headers={'Authorization': f'Bearer {token2}'})
    assert response.status_code == 404

    # User2 tenta deletar
    response = client.delete(f'/movies/{movie_id}', headers={'Authorization': f'Bearer {token2}'})
    assert response.status_code == 404


def test_movies_require_authentication(client):
    response = client.get('/movies')
    assert response.status_code == 401

    response = client.post('/movies', json={'title': 'Teste'})
    assert response.status_code == 401
