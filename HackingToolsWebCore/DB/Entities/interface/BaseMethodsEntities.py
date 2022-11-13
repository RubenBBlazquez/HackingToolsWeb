from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class IEntity(ABC):
    """
        Interface with base methods that will have all entities
    """

    @abstractmethod
    def get_table(self) -> str:
        """
            Method to know from which table is an entity

            :return: table_name
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
            Method to transform an object into a dict

            :return: dict
        """
        pass

    @abstractmethod
    def create_object(self, data) -> IEntity:
        """
            Method to transform an object into a dict

            :return: IEntity
        """
        pass
