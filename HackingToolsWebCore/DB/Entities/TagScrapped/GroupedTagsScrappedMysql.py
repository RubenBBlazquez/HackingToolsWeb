from ..interface.BaseMethodsEntities import IEntity


class GroupedTagsScrapped(IEntity):

    def get_table(self) -> str:
        return self._table

    def __init__(self):
        self._table = "TAGS_FROM_WEB_SCRAPPED"
        self._tag = ""
        self._web_scrapped = ""
        self._endpoint_web_scrapped = ""
        self._count = 0

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
        return {'TAG': self._tag, 'COUNT': self._count,
                'WEB_SCRAPPED': self._web_scrapped,
                'ENDPOINT_WEB_SCRAPPED': self._endpoint_web_scrapped}

    def create_object(self, data):

        if 'TAG' in data and data['TAG']:
            self.setTag(data['TAG'])

        if 'COUNT' in data and data['COUNT']:
            self.setCount(data['COUNT'])

        if 'WEB_SCRAPPED' in data and data['WEB_SCRAPPED']:
            self.setWebScrapped(data['WEB_SCRAPPED'])

        if 'ENDPOINT_WEB_SCRAPPED' in data and data['ENDPOINT_WEB_SCRAPPED']:
            self.setEndpointWebScrapped(data['ENDPOINT_WEB_SCRAPPED'])

        return self
