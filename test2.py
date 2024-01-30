from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Test(BaseModel):
    id: int = 1
    text: str = "BBBB"

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: list[str] = []
    text: list = Test()


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
    