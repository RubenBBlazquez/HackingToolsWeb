from enum import Enum
from typing import Type

from ..interface.BaseMethodsEntities import IEntity


class AttributeLiterals(Enum):
    TAG = 'tag'
    TAG_INFO = 'tagInfo'
    WEB_SCRAPPED = 'webScrapped'
    ENDPOINT_WEB_SCRAPPED = 'endpointWebScrapped'


class TagScrapped(IEntity):

    def get_table(self) -> str:
        return self._table

    def __init__(self):
        self._table = "TagsFromWebsScrapped"
        self._tag = ""
        self._tag_info = ""
        self._web_scrapped = ""
        self._endpoint_web_scrapped = ""
        self.literals = AttributeLiterals

    def getTag(self):
        return self._tag

    def setTag(self, tag):
        self._tag = tag
        return self

    def getTagInfo(self):
        return self._tag_info

    def setTagInfo(self, tag_info):
        self._tag_info = tag_info
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
        return {self.literals.TAG.value: self._tag,
                self.literals.TAG_INFO.value: self._tag_info,
                self.literals.WEB_SCRAPPED.value: self._web_scrapped,
                self.literals.ENDPOINT_WEB_SCRAPPED.value: self._endpoint_web_scrapped}

    def get_attribute_list_with_types(self, discard_columns: list = []) -> list:
        tag = self.literals.TAG.value + '-' + str(type(self.getTag()))
        tag_info = self.literals.TAG_INFO.value + '-' + str(type(self.getTagInfo()))
        web_scrapped = self.literals.WEB_SCRAPPED.value + '-' + str(type(self.getWebScrapped()))
        endpoint = self.literals.ENDPOINT_WEB_SCRAPPED.value + '-' + str(type(self.getEndpointWebScrapped()))

        return [tag, tag_info, web_scrapped, endpoint]

    def get_attributes_enum(self) -> Type[AttributeLiterals]:
        return self.literals

    def create_object(self, data):
        if self.literals.TAG.value in data and data[self.literals.TAG.value]:
            self.setTag(data[self.literals.TAG.value])

        if self.literals.TAG_INFO.value in data and data[self.literals.TAG_INFO.value]:
            self.setTagInfo(data[self.literals.TAG_INFO.value])

        if self.literals.WEB_SCRAPPED.value in data and data[self.literals.WEB_SCRAPPED.value]:
            self.setWebScrapped(data[self.literals.WEB_SCRAPPED.value])

        if self.literals.ENDPOINT_WEB_SCRAPPED.value in data and data[self.literals.ENDPOINT_WEB_SCRAPPED.value]:
            self.setEndpointWebScrapped(data[self.literals.ENDPOINT_WEB_SCRAPPED.value])

        return self
