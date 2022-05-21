from typing import Any
from HackingToolsWeb.DB.Databases.interface.IDBMethods import IDBActions
from HackingToolsWeb.DB.Entities.interface.BaseMethodsEntities import IEntity


class ElasticSearchDB(IDBActions):

    def __init__(self):
        self.elastic_db_instance = None

    # singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def get_connection(self) -> Any:
        pass

    def select_one(self, filter_query: str, entity: IEntity) -> Any:
        pass

    def select_many(self) -> list:
        pass

    def delete(self) -> Any:
        pass

    def update(self) -> Any:
        pass

    def insert(self, entity: IEntity) -> None:
        pass
