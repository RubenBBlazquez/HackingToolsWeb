from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from HackingToolsWeb.DB.Entities.interface.BaseMethodsEntities import IEntity


class IDBMethods(ABC):
    """
    The Builder interface specifies methods for creating the different parts of a database
    """

    @abstractmethod
    def get_connection(self) -> Any:
        pass

    @abstractmethod
    def select_one(self, sql: str, entity: IEntity) -> Any:
        pass

    @abstractmethod
    def select_many(self) -> list:
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
