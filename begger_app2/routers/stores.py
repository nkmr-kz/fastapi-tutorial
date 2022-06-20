from fastapi import APIRouter, Depends
from repositories.database import yield_db
from sqlalchemy.orm import Session
from usecases import stores_usecase

router = APIRouter(
  prefix="",
  tags=["stores"],
  responses={404: {"description": "Not found"}}
)

@router.get("/stores")
def read_users(db:Session = Depends(yield_db)):
    return stores_usecase.find_users(db)
