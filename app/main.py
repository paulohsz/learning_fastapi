from fastapi import FastAPI

from app.schemas import Message

app = FastAPI()


@app.get('/', response_model=Message)
async def read_root():
    return {'message': 'Hello World'}


@app.get('/items/{item_id}')
async def read_item(item_id: int, q: str = None):
    return {'item_id': item_id, 'q': q}
