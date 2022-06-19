from fastapi import Depends, FastAPI

from .dependencies import get_token_header
from .routers import users

app = FastAPI(dependencies=[Depends(get_token_header)])

app.include_router(users.router)

@app.get("/",tags=["root"])
def read_root():
    return {"Hello": "World"}
