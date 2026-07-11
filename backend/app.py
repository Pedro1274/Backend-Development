from fastapi import (  # ty:ignore[unresolved-import]
    FastAPI,
)
from fastapi.responses import HTMLResponse

from backend.routers import auth, users
from backend.schemas import Message

app = FastAPI(title='Our cool and fast API')

app.include_router(auth.router)
app.include_router(users.router)


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
