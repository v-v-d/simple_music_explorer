"""
Test the Auth operations
"""
import http.client
from unittest.mock import ANY

from faker import Faker

from auth_backend.models import UserModel
from .utils import (
    register_user, activate_user, create_login_user, get_headers,
    delete_user, get_login_user_from_register_user
)

fake = Faker()


def test_register(client, app):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_register_bad_email(client, app):
    response, new_user = register_user(client, bad_email=True)

    assert http.client.BAD_REQUEST == response.status_code

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_register_bad_password_2(client, app):
    response, _ = register_user(client, bad_password_2=True)

    assert http.client.BAD_REQUEST == response.status_code


def test_activate(client):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    response = activate_user(client, new_user['username'])

    assert http.client.OK == response.status_code

    expected = {
        'Authorized': ANY,
    }
    assert response.json == expected

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_activate_bad_uname64(client):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    response = activate_user(client, new_user['username'], bad_uname64=True)

    assert http.client.BAD_REQUEST == response.status_code

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_activate_bad_token(client):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    response = activate_user(client, new_user['username'], bad_token=True)

    assert http.client.BAD_REQUEST == response.status_code

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_login(client):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    username = new_user['username']
    response = activate_user(client, new_user['username'])

    assert http.client.OK == response.status_code

    user_id = fake.pyint()
    headers = get_headers(username, user_id)

    response = client.post('/api/auth/logout/', headers=headers)
    result = response.json

    assert http.client.OK == response.status_code

    expected = {
        'Authorized': None,
    }

    assert result == expected

    new_user = get_login_user_from_register_user(new_user)

    response = client.post('/api/auth/login/', data=new_user)
    result = response.json

    assert http.client.OK == response.status_code

    expected = {
        'Authorized': ANY,
    }
    assert result == expected

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_login_unknown_user(client):
    new_user = create_login_user()
    response = client.post('/api/auth/login/', data=new_user)
    assert http.client.UNAUTHORIZED == response.status_code


def test_login_user_not_active(client):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    new_user = get_login_user_from_register_user(new_user)

    response = client.post('/api/auth/login/', data=new_user)

    assert http.client.UNAUTHORIZED == response.status_code

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_login_bad_password(client):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    username = new_user['username']
    response = activate_user(client, new_user['username'])

    assert http.client.OK == response.status_code

    user_id = fake.pyint()
    headers = get_headers(username, user_id)

    response = client.post('/api/auth/logout/', headers=headers)
    result = response.json

    assert http.client.OK == response.status_code

    expected = {
        'Authorized': None,
    }

    assert result == expected

    user_data = get_login_user_from_register_user(new_user)
    user_data['password'] = ''

    response = client.post('/api/auth/login/', data=user_data)
    assert http.client.UNAUTHORIZED == response.status_code

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_logout_unauthorized(client):
    response = client.post('/api/auth/logout/')
    assert http.client.UNAUTHORIZED == response.status_code


def test_delete_unauthorized(client):
    password = fake.password(length=15, special_chars=True)
    response = client.delete('/api/auth/', data={'password': password})

    assert http.client.UNAUTHORIZED == response.status_code


def test_delete_bad_user_id(client):
    user_data = create_login_user()
    response = delete_user(client, user_data)

    assert http.client.NO_CONTENT == response.status_code


def test_delete_bad_password(client):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    response = activate_user(client, new_user['username'])

    assert http.client.OK == response.status_code

    response = delete_user(client, new_user, bad_password=True)

    assert http.client.BAD_REQUEST == response.status_code

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_get_user_unauthorized(client):
    response = client.get('/api/auth/')
    assert http.client.UNAUTHORIZED == response.status_code


def test_get_user(client):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    username = new_user['username']
    response = activate_user(client, username)

    assert http.client.OK == response.status_code

    user = UserModel.query.filter_by(name=username).first()
    headers = get_headers(username, user.id)
    response = client.get('/api/auth/', headers=headers)
    result = response.json

    assert http.client.OK == response.status_code

    expected = {
        'id': ANY,
        'name': username,
        'password': ANY,
        'email': new_user['email'],
    }

    assert result == expected

    response = delete_user(client, new_user)

    assert http.client.NO_CONTENT == response.status_code


def test_get_user_unknown_user(client):
    username = fake.first_name()
    user_id = fake.pyint()
    headers = get_headers(username, user_id)
    response = client.get('/api/auth/', headers=headers)

    assert http.client.NOT_FOUND == response.status_code


def test_delete_admin(client):
    response, new_user = register_user(client)

    assert http.client.OK == response.status_code

    username = new_user['username']
    response = activate_user(client, username)

    assert http.client.OK == response.status_code

    user = UserModel.query.filter_by(name=username).first()
    response = client.delete(f'/admin/auth/{user.id}/')

    assert http.client.NO_CONTENT == response.status_code
