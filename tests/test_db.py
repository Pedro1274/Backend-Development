from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from backend.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User, time=datetime.now()) as time:
        user = User(username='teste', email='teste@teste.com', password='1234')

        session.add(user)
        session.commit()

    user = session.scalar(select(User).where(User.password == '1234'))

    assert asdict(user) == {
        'id': 1,
        'username': 'teste',
        'email': 'teste@teste.com',
        'password': '1234',
        'created_at': time,
        'updated_at': time,
    }
