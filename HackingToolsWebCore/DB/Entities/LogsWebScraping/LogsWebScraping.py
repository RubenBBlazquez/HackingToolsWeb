import time
from ..interface.BaseMethodsEntities import IEntity


class LogsWebScraping(IEntity):

    def __init__(self):
        self._table = "LogWebsScrapped"
        self._log_date = time.strftime('%Y-%m-%d %H:%M:%S')
        self._base_url = ""
        self._endpoint = ""
        self._log_error = ""

    def get_table(self) -> str:
        return self._table

    def getLogDate(self) -> str:
        return self._log_date

    def setLogDate(self, log_date: str):
        self._log_date = log_date
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

    def getLogError(self) -> str:
        return self._endpoint

    def setLogError(self, log_error: str):
        self._log_error = log_error
        return self

    def to_dict(self) -> dict:
        return {'logDate': self._log_date, 'baseUrl': self._base_url,
                'endpoint': self._endpoint,
                'logError': self._log_error}

    def create_object(self, data):

        if 'logDate' in data and data['logDate']:
            self.setLogDate(data['logDate'])

        if 'baseUrl' in data and data['baseUrl']:
            self.setBaseUrl(data['baseUrl'])

        if 'endpoint' in data and data['endpoint']:
            self.setEndpoint(data['endpoint'])

        if 'logError' in data and data['logError']:
            self.setLogError(data['logError'])

        return self
