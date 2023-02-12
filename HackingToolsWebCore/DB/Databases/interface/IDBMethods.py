from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from HackingToolsWebCore.DB.Entities.interface.BaseMethodsEntities import IEntity


class IDBActions(ABC):
    """
    The Builder interface specifies methods for creating the different parts of a database
    """

    @abstractmethod
    def get_connection(self) -> Any:
        pass

    @abstractmethod
    def select_one(self, filter_query: str, entity: IEntity) -> Any:
        pass

    @abstractmethod
    def select_many(self, select_values: list, query_values: list[tuple], entity: IEntity, limit: str,
                    offset: str) -> list:
        pass

    @abstractmethod
    def grouped_select(self, select_values: list,  query_values: list[tuple], entity: IEntity, limit: str,
                       offset: str) -> list:
        pass

    @abstractmethod
    def delete(self) -> Any:
        pass

    @abstractmethod
    def update(self) -> Any:
        pass

    @abstractmethod
    def insert(self, entity: IEntity) -> None:
        pass
