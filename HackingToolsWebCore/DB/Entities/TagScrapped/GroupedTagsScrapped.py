from enum import Enum
from typing import Type

from ..interface.BaseMethodsEntities import IEntity


class AttributeLiterals(Enum):
    TAG = 'tag'
    COUNT = 'count'
    WEB_SCRAPPED = 'webScrapped'
    ENDPOINT_WEB_SCRAPPED = 'endpointWebScrapped'


class GroupedTagsScrapped(IEntity):

    def get_table(self) -> str:
        return self._table

    def __init__(self):
        self._table = "TagsFromWebsScrapped"
        self._tag = ""
        self._web_scrapped = ""
        self._endpoint_web_scrapped = ""
        self._count = 0
        self.literals = AttributeLiterals

    def getTag(self):
        return self._tag

    def setTag(self, tag):
        self._tag = tag
        return self

    def getCount(self):
        return self._count

    def setCount(self, count):
        self._count = count
        return self

    def getWebScrapped(self):
        return self._web_scrapped

    def setWebScrapped(self, web_scrapped):
        self._web_scrapped = web_scrapped
        return self

    def getEndpointWebScrapped(self):
        return self._endpoint_web_scrapped

    def setEndpointWebScrapped(self, endpoint_web_scrapped):
        self._endpoint_web_scrapped = endpoint_web_scrapped
        return self

    def to_dict(self) -> dict:
        return {'tag': self._tag, 'count': self._count,
                'webScrapped': self._web_scrapped,
                'endpointWebScrapped': self._endpoint_web_scrapped}

    def get_attributes_enum(self) -> Type[AttributeLiterals]:
        return self.literals

    def create_object(self, data):

        if self.literals.TAG.value in data and data[self.literals.TAG.value]:
            self.setTag(data[self.literals.TAG.value])

        if self.literals.COUNT.value in data and data[self.literals.COUNT.value]:
            self.setCount(data[self.literals.COUNT.value])

        if self.literals.WEB_SCRAPPED.value in data and data[self.literals.WEB_SCRAPPED.value]:
            self.setWebScrapped(data[self.literals.WEB_SCRAPPED.value])

        if self.literals.ENDPOINT_WEB_SCRAPPED.value in data and data[self.literals.ENDPOINT_WEB_SCRAPPED.value]:
            self.setEndpointWebScrapped(data[self.literals.ENDPOINT_WEB_SCRAPPED.value])

        return self
