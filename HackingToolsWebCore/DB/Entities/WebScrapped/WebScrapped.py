import time
from enum import Enum
from typing import Type

from ..interface.BaseMethodsEntities import IEntity


class AttributeLiterals(Enum):
    BASE_URL = 'baseUrl'
    ENDPOINT = 'endpoint'
    SCRAP_DATE = 'scrapDate'
    IS_SCRAP_FINISHED = 'isScrapFinished'


class WebScrapped(IEntity):

    def __init__(self):
        self._table = "WebsScrapped"
        self._scrap_date = time.strftime('%Y-%m-%d %H:%M:%S')
        self._base_url = ""
        self._endpoint = ""
        self._scrap_finished = False
        self.literals = AttributeLiterals

    def getScrapDate(self) -> str:
        return self._scrap_date

    def get_table(self) -> str:
        return self._table

    def setScrapDate(self, scrap_date: str):
        self._scrap_date = scrap_date
        return self

    def getBaseUrl(self) -> str:
        return self._base_url

    def setBaseUrl(self, base_url: str):
        self._base_url = base_url
        return self

    def getEndpoint(self) -> str:
        return self._endpoint

    def setEndpoint(self, endpoint):
        self._endpoint = endpoint
        return self

    def isScrapFinished(self) -> bool:
        return self._scrap_finished

    def setScrapFinished(self, scrap_finished: bool):
        self._scrap_finished = scrap_finished
        return self

    def get_attributes_enum(self) -> Type[AttributeLiterals]:
        return self.literals

    def to_dict(self) -> dict:
        return {self.literals.SCRAP_DATE.value: self._scrap_date,
                self.literals.BASE_URL.value: self._base_url,
                self.literals.ENDPOINT.value: self._endpoint,
                self.literals.IS_SCRAP_FINISHED.value: self._scrap_finished}

    def create_object(self, data):

        if data[self.literals.SCRAP_DATE.value]:
            self.setScrapDate(data[self.literals.SCRAP_DATE.value])

        if data[self.literals.BASE_URL.value]:
            self.setBaseUrl(data[self.literals.BASE_URL.value])

        if data[self.literals.ENDPOINT.value]:
            self.setEndpoint(data[self.literals.ENDPOINT.value])

        if data[self.literals.IS_SCRAP_FINISHED.value]:
            self.setScrapFinished(data[self.literals.IS_SCRAP_FINISHED.value])

        return self
