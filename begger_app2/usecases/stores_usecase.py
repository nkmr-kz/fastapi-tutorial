from typing import List

from fastapi import Depends
from repositories.database import Base, engine, yield_db
from repositories.db_schema.store_schema import StoreSchema
from repositories.store_repository import find_stores
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

def find_users(db:Session)->List[StoreSchema]:
    return find_stores(db)
