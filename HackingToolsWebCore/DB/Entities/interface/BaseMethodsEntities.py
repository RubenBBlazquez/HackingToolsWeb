from __future__ import annotations
from abc import ABC, abstractmethod


class IEntity(ABC):
    """
        Interface with base methods that will have all entities
    """

    @abstractmethod
    def get_table(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
            Method to transform a object into a dict

            :return dict
        """
        pass

    @abstractmethod
    def create_object(self, data) -> IEntity:
        """
            Method to transform a object into a dict
        """
        pass
