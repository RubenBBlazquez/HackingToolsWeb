from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class ICacheMethods(ABC):
    @abstractmethod
    def get_instance(self) -> Any:
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def put(self, key: str, value: Any) -> Any:
        pass

    @abstractmethod
    def clear_cache_with_seconds(self, seconds: int) -> bool:
        pass

    @abstractmethod
    def clear_cache(self) -> bool:
        pass
