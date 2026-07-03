from fastapi import FastAPI, HTTPException  # ty:ignore[unresolved-import]
from fastapi.responses import HTMLResponse

from backend.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title='Our cool and fast API')
database = []


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
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=200, response_model=UserList)
def get_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database))

    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=404, detail='Usuário não encontrado!')

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=UserPublic)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=404, detail='Usuário não encontrado!')

    return database.pop(user_id - 1)
