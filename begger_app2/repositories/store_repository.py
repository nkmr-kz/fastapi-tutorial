# import abc

from sqlalchemy.orm import Session

from .db_models.stores import Store

# class StoreRepository(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def find_stores(self):
#         pass


def find_stores(db: Session):
    return db.query(Store).all()
