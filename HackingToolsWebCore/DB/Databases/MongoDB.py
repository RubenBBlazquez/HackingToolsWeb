import os
from typing import Any
from HackingToolsWebCore.DB.Databases.interface.IDBMethods import IDBActions
from HackingToolsWebCore.DB.Entities.interface.BaseMethodsEntities import IEntity
import pymongo

class MongoDB(IDBActions):

    def __init__(self):
        self.mongoDBClient = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_URL"))
        self.database = self.mongoDBClient.get_database()

    # singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def get_connection(self) -> Any:
        return self.mongoDBClient

    def select_one(self, filter_query: str, entity: IEntity) -> Any:
        pass

    def select_many(self, prepared_values: tuple, entity: IEntity) -> list:
        pass

    def delete(self) -> Any:
        pass

    def update(self) -> Any:
        pass

    def insert(self, entity: IEntity) -> None:
        pass
