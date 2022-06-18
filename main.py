import time
from re import A
from typing import Union
from fastapi import Body, FastAPI, Query, Path, Request, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Process time: {process_time}")    
    return response


class Item(BaseModel):
    name: str = Field(
        description= "The name of the item",
        max_length=100,
    )
    price: float
    tsgs: list
    url: HttpUrl

class Name(BaseModel):
    firstName: str
    LastName: str

class User(BaseModel):
    name: Name
    email: str        
    password: str

class UnicornException(Exception):
    def __init__(self, message: str):
        self.message = message
        
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(status_code=418, content={"detail": exc.message})

@app.get("/errors",tags=["errors"])
async def get_errors():
    raise HTTPException(status_code=400, detail="Bad Request")

@app.get("/unicorn-errors",tags=["errors"])
async def get_unicorn_errors():
    raise UnicornException("This is a unicorn error")

@app.post("/files",tags=["files"])
async def create_file(file: UploadFile):
    return {"file_size": file.filename}

@app.post("/users/items",response_model=Item,tags=["users"])
async def create_item(item: Item,user: User = Body(description="test body"),singleBody: int = Body()):
    return {"item": item, "user": user, "singleBody": singleBody}

@app.get("/",tags=["root"])
async def root():
    """
    Message: Hello World
    
    - **message**: Hello World

    """
    return {"message": "Hello World"}


@app.post("/items/{item_id}",tags=["items"])
async def create_item(item_id: int, item: Item):
    item_id:int = Path(title="Item ID", description="The ID of the item to get", generic=True, example=1)
    print(item_id)
    print(item.dict())
    return {"item_id": item_id, **item.dict()}


@app.get("/items/{item_id}",tags=["items"])
async def read_item(
    item_id: int,
    q: Union[str, None] = Query(
        default=None,
        max_length=10,
        regex="^[a-z]",
        title="title",
        description="test query"
        )
    ):
    return {"item_id": item_id, "q": q}


@app.get("/items/{item_id}/lists",tags=["items"])
async def read_item_list(
    item_id: int,
    q: list = Query(default=[])):
    return {"item_id": item_id, "q": q}
