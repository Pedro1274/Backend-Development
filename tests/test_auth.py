from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'testando123'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha não autorizados!'}


def test_get_inexistent_user(client):
    response = client.post(
        '/auth/token',
        data={'username': 'uzuario1', 'password': 'testando123'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha não autorizados!'}


def test_token_expired_after_time(client, user):
    with freeze_time('2026-12-31 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2026-12-31 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'mr_wong',
                'email': 'mr_wong@email.com',
                'password': 'immrwong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {
            'detail': 'Não foi possível validar as credenciais!'
        }


def test_refresh_token(client, user, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {
            'detail': 'Não foi possível validar as credenciais!'
        }
