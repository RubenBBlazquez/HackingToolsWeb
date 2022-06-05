import time
from ..interface.BaseMethodsEntities import IEntity


class LogsWebScraping(IEntity):

    def __init__(self):
        self._table = "LOGS_WEBS_SCRAPPED"
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
        return {'TABLE_NAME': self._table, 'LOG_DATE': self._log_date, 'BASE_URL': self._base_url,
                'ENDPOINT': self._endpoint,
                'LOG_ERROR': self._log_error}

    def create_object(self, data):

        if data['LOG_DATE']:
            self.setLogDate(data['LOG_DATE'])

        if data['BASE_URL']:
            self.setBaseUrl(data['BASE_URL'])

        if data['ENDPOINT']:
            self.setEndpoint(data['ENDPOINT'])

        if data['LOG_ERROR']:
            self.setLogError(data['LOG_ERROR'])

        return self
