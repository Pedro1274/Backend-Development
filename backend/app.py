from fastapi import FastAPI  # ty:ignore[unresolved-import]
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/', status_code=200)
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