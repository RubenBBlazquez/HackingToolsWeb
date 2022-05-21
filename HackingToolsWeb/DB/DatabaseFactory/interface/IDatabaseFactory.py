from __future__ import annotations
from abc import ABC, abstractmethod
from HackingToolsWeb.DB.Databases.interface.IDBMethods import IDBActions
from ..Enum.DatabaseTypesEnum import DATABASE_TYPES


class IDatabaseFactory(ABC):
    """
        The Builder interface specifies methods for creating the different parts of a database
    """

    @abstractmethod
    def get_database(self, db_type: DATABASE_TYPES) -> IDBActions:
        pass
