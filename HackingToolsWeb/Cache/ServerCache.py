from typing import Any
from diskcache import Cache
from django.utils.translation import override
from .interface.ICacheMethods import ICacheMethods
from ..SingletonMetaFile.SingletonMeta import SingletonMeta
import time


class CacheMethodsImplement(ICacheMethods):

    def __init__(self, cache_instance: Cache):
        self.cache = cache_instance
        self.last_time_cache_cleared = int(time.time())

    def get_instance(self) -> Any:
        return self.cache

    def get(self, key) -> Any:
        return self.cache.get(key)

    def put(self, key, value) -> Any:
        return self.cache.set(key, value)

    def clear_cache_with_seconds(self, seconds) -> bool:
        if (int(time.time()) - self.last_time_cache_cleared) >= seconds:
            self.last_time_cache_cleared = int(time.time())
            self.cache.clear(retry=True)
            print("clear")
            return True

        return False

    def clear_cache(self):
        self.cache.clear(retry=True)


class ServerCache(metaclass=SingletonMeta):

    def __init__(self):
        self.cache = Cache()

    def get_builder(self):
        return CacheMethodsImplement(self.cache)
