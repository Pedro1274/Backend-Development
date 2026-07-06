from http import HTTPStatus

from fastapi import (  # ty:ignore[unresolved-import]
    Depends,
    FastAPI,
    HTTPException,
)
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.database import get_session
from backend.models import User
from backend.schemas import Message, UserList, UserPublic, UserSchema
from backend.security import get_password_hash

app = FastAPI(title='Our cool and fast API')


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Hello, world!'}


@app.get('/pretty_root', status_code=200, response_class=HTMLResponse)
def read_pretty_root():
    return """
    <html>
        <head>
            <title>Our new Hello world!</title>
        </head>
        <body>
            <h1>Hello, world!</h1>
        </body>
    </html>"""


@app.post('/users/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='Usuário já existente!', status_code=HTTPStatus.CONFLICT
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail='Email já existente!', status_code=HTTPStatus.CONFLICT
            )

    db_user = User(
        username=user.username, password=get_password_hash(user.password), email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=200, response_model=UserList)
def get_users(limit: int = 10, offset: int = 0, session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get('/users/{user_id}', response_model=UserPublic)
def get_single_user(user_id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            detail='Usuário não encontrado', status_code=HTTPStatus.NOT_FOUND
        )
    return user_db


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            detail='Usuário não encontrado', status_code=HTTPStatus.NOT_FOUND
        )
    try:
        user_db.email = user.email
        user_db.username = user.username
        user_db.password = get_password_hash(user.password)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            detail='Usuário ou Email já existentes!',
            status_code=HTTPStatus.CONFLICT,
        )


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            detail='Usuário não encontrado', status_code=HTTPStatus.NOT_FOUND
        )
    session.delete(user_db)
    session.commit()

    return {'message': 'Usuário deletado com sucesso!'}
