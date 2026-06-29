from fastapi import FastAPI  # ty:ignore[unresolved-import]

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Hello, world!'}
