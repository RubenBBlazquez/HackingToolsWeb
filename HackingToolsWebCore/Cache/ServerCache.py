from typing import Any
from diskcache import Cache
from .interface.ICacheMethods import ICacheMethods
from HackingToolsWebCore.MetaFiles.SingletonMetaFile.SingletonMeta import SingletonMeta
import time


class ServerCache(ICacheMethods):

    # singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.cache = Cache()
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
