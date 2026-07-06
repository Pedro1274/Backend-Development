from http import HTTPStatus

from backend.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')

    assert response.json() == {'message': 'Hello, world!'}
    assert response.status_code == HTTPStatus.OK


def test_pretty_root_deve_retornar_ola_mundo(client):

    response = client.get('/pretty_root')

    assert response.status_code == HTTPStatus.OK

    expected_html = """<html>
        <head>
            <title>Our new Hello world!</title>
        </head>
        <body>
            <h1>Hello, world!</h1>
        </body>
    </html>"""
    assert response.text.strip() == expected_html.strip()


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': '1234',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_create_same_username_integrity_error(client, user):
    response_update = client.post(
        '/users/',
        json={
            'username': 'Alice',
            'email': 'naoeemaildaalice@test.com',
            'password': '1234',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Usuário já existente!'}


def test_create_same_email_integrity_error(client, user):
    response_update = client.post(
        '/users/',
        json={
            'username': 'naoeaalice',
            'email': 'Alice@alice.com',
            'password': '1234',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Email já existente!'}


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_single_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Alice',
        'email': 'Alice@alice.com',
        'id': 1,
    }


def test_read_single_user_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_not_found(client, token):
    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': '1234',
        },
    )

    # Aqui precisamos de uma conta de administrador para encontrar o 404
    # assert response.status_code == HTTPStatus.NOT_FOUND
    # assert response.json() == {'detail': 'Usuário não encontrado'}
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Sem permissões suficientes!'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado com sucesso!'}


def test_delete_user_not_found(client, token):
    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
    )

    # assert response.status_code == HTTPStatus.NOT_FOUND
    # assert response.json() == {'detail': 'Usuário não encontrado'}
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Sem permissões suficientes!'}


def test_update_integrity_error(client, user, token):
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': '1234',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': '12345',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Usuário ou Email já existentes!'
    }


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
