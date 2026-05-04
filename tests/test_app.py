import pytest
from src.app import create_app
from src.models import db
from src.models.user import User


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key',
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
