from http import HTTPStatus

from fastapi.testclient import TestClient

from backend.app import app


def test_root_deve_retornar_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Hello, world!'}
    assert response.status_code == HTTPStatus.OK


def test_pretty_root_deve_retornar_ola_mundo():
    client = TestClient(app)

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
