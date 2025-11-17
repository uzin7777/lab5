from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'unknown@mail.com'})
    assert response.status_code == 404
    json_data = response.json()
    assert 'detail' in json_data

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {'name': 'Sergey Sergeev', 'email': 'sergey.sergeev@mail.com'}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    created_id = response.json()
    assert isinstance(created_id, int)

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    duplicate = {'name': 'Ivan Test', 'email': users[0]['email']}
    response = client.post("/api/v1/user", json=duplicate)
    assert response.status_code in (400, 409)
    json_data = response.json()
    assert 'detail' in json_data

def test_delete_user():
    '''Удаление пользователя'''
    test_email = 'delete.me@mail.com'
    create = client.post("/api/v1/user", json={'name': 'Delete Me', 'email': test_email})
    assert create.status_code == 201
    response = client.delete("/api/v1/user", params={'email': test_email})
    assert response.status_code == 204
    check = client.get("/api/v1/user", params={'email': test_email})
    assert check.status_code == 404

