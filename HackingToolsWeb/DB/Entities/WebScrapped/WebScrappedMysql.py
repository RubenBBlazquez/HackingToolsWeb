import time
from ..interface.BaseMethodsEntities import IEntity


class WebScrapped(IEntity):

    def __init__(self):
        self._table = "WEBS_SCRAPPED"
        self._scrap_date = time.strftime('%Y-%m-%d %H:%M:%S')
        self._base_url = ""
        self._endpoint = ""
        self._scrap_finished = False

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

    def to_dict(self) -> dict:
        return {'TABLE_NAME': self._table, 'SCRAP_DATE': self._scrap_date, 'BASE_URL': self._base_url,
                'ENDPOINT': self._endpoint,
                'SCRAP_FINISHED': self._scrap_finished}

    def create_object(self, data):

        if data['SCRAP_DATE']:
            self.setScrapDate(data['SCRAP_DATE'])

        if data['BASE_URL']:
            self.setBaseUrl(data['BASE_URL'])

        if data['ENDPOINT']:
            self.setEndpoint(data['ENDPOINT'])

        if data['SCRAP_FINISHED']:
            self.setScrapFinished(data['SCRAP_FINISHED'])

        return self
