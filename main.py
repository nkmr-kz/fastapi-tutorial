from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    print(item_id)
    print(item.dict())
    return {"item_id": item_id, **item.dict()}
