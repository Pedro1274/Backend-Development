from http import HTTPStatus

from backend.schemas import UserPublic


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
            'username': 'test2',
            'email': 'test2@test.com',
            'password': '1234',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Usuário já existente!'}


def test_create_same_email_integrity_error(client, user):
    response_update = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'test3@test.com',
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
        'username': 'test5',
        'email': 'test5@test.com',
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


def test_update_user_not_found(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
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


def test_delete_user_not_found(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
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
