import json

from ..interface.BaseMethodsEntities import IEntity


class EndpointAlreadySniffed(IEntity):

    def __init__(self):
        self._table = "SNIFFED_ENDPOINTS"
        self._endpoint = ""
        self._information = []

    def get_table(self) -> str:
        return self._table

    def set_endpoint(self, endpoint: str):
        self._endpoint = endpoint

        return self

    def set_information(self, information: list):
        self._information = information

        return self

    def to_dict(self) -> dict:
        return {'TABLE_NAME': self._table, 'endpoint': self._endpoint, 'information': self._information}

    def create_object(self, data):

        if data['ENDPOINT']:
            self.set_endpoint(data['ENDPOINT'])

        if data['INFORMATION']:
            self.set_information(json.loads(data['INFORMATION']))

        return self
