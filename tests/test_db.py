from sqlalchemy import select

from backend.models import User


def test_create_user(session):
    user = User(username='teste', email='teste@teste.com', password='1234')

    session.add(user)
    session.commit()

    user = session.scalar(select(User).where(User.password == '1234'))

    assert user.password == '1234'
