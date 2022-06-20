from pydantic import BaseModel


class StoreSchema(BaseModel):
    id: int
    sotre_name: str

    class Config:
        orm_mode = True
