import os
from typing import Any
from HackingToolsWebCore.DB.Databases.interface.IDBMethods import IDBActions
from HackingToolsWebCore.DB.Entities.interface.BaseMethodsEntities import IEntity
import pymongo

class MongoDB(IDBActions):

    def __init__(self):
        self.mongoDBClient = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_URL"))
        self.database = self.mongoDBClient.get_database(os.getenv('MONGO_DATABASE'))

    # singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def get_connection(self) -> Any:
        return self.mongoDBClient

    def select_one(self, filter_query: str, entity: IEntity) -> Any:
        collection = self.database.get_collection(entity.get_table())

        return collection.find_one(filter_query)

    def select_many(self, select_values: list, prepared_information: dict, entity: IEntity, limit: str,
                    offset: str) -> list:

        pass

    def delete(self) -> Any:
        pass

    def update(self) -> Any:
        pass

    def insert(self, entity: IEntity) -> None:
        pass
