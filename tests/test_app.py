from http import HTTPStatus


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
