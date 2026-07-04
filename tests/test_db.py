from backend.models import User


def test_create_user(session):
    user = User(username='teste', email='teste@teste.com', password='1234')

    session.add(user)
    session.commit()

    assert user.password == '1234'
