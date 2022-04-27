from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class IDBMethods(ABC):
    """
    The Builder interface specifies methods for creating the different parts of a database
    """

    @abstractmethod
    def get_connection(self) -> Any:
        pass

    @abstractmethod
    def select_one(self, sql) -> Any:
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
