from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

items = [
    {'id':1, 'data':'apple', 'color':'red'},
    {'id':2, 'data':'banana', 'color':'yellow'},
    {'id':3, 'data':'cherry', 'color':'red'}
]

class ItemCreate(BaseModel):
    data: str
    color: str

@app.post('/items')
def create_item(payload: ItemCreate):
    item = {'id': len(items)+1, **payload.model_dump()}
    items.append(item)
    return item

@app.get('/items/{item_id}')
def get_item_by_id(item_id: int):
    for item in items:
        if item.get('id') == item_id:
            return item
    raise HTTPException(status_code=404, detail='Item not found')

@app.get('/items')
def search_items(q: Optional[str] = None):
    result = [item for item in items if q in item.get('data')]
    if result:
        return result
    raise HTTPException(status_code=404, detail='Item not found')
