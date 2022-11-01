import json
import os.path
from typing import Any
import pandas as pd
import numpy as np
from HackingToolsWebCore.Utils.Utils import Utils
from HackingToolsWebCore.settings import Database
from HackingToolsWebCore.DB.Entities.EndpointsAlreadySniffed.EndpointAlreadySniffedMysql import EndpointAlreadySniffed


class FileCreator:
    _dictionary = {}
    _absolute_path = os.path.abspath(os.getcwd())

    def __init__(self, dictionary=None, get_default_file=True):
        self._dictionary = FileCreator.get_default_endpoints_dictionary() if get_default_file else dictionary
        print(self._dictionary)

    def get_xls_file(self, main_dict_key='Endpoints') -> str:
        """
            Method to transform a default dict into an Excel

            :param main_dict_key: param to know for what key we have to normalize

            :return file dir
        """

        file_dir = self._absolute_path + '\\dictionary.xlsx'

        # con json_normalize transformamos un json (dict) en un dataframe,
        # y con recordPath sacamos las keys de dentro de ese array
        dataframe = pd.json_normalize(self._dictionary, record_path=main_dict_key)

        # we create the xls file
        dataframe.to_excel(file_dir, index=False)

        return file_dir

    def get_json_file(self, main_dict_key) -> str:
        """
            Method to transform a default dict into a json

            :param main_dict_key: param to know for what key we have to normalize

            :return file dir
        """

        file_dir = self._absolute_path + '\\dictionary.json'

        # con json_normalize transformamos un json (dict) en un dataframe,
        # y con recordPath sacamos las keys de dentro de ese array
        dataframe = pd.json_normalize(self._dictionary, record_path=main_dict_key)

        # we create the json file
        dataframe.to_json(file_dir, index=False)

        return file_dir

    def get_default_file_by_type(self, file_type: str, main_dict_key='Endpoints') -> str:
        """

        """

        excel_types = ['excel', 'xls', 'xlsx']

        if file_type not in excel_types:
            return self.get_json_file(main_dict_key)

        return self.get_xls_file(main_dict_key)

    @staticmethod
    def get_default_endpoints_dictionary() -> dict:
        default_url = 'http://127.0.0.1:8000/'

        return {
            'Endpoints': [
                {
                    'url': default_url,
                    "Endpoint": 'v1/example',
                    'customHeaders': "{'content-type': 'application/json', 'Accept-Language': 'en'}",
                    "Optional auth type": 'bearer',
                    "auth": 'Bearer xxxx'
                },
                {
                    'url': default_url,
                    "Endpoint": 'v1/example2',
                    'customHeaders': "{'content-type': 'application/json', 'Accept-Language': 'en'}",
                    "Optional auth type": 'basic',
                    "auth": 'cHJ1ZWJhMTIzMTM='
                },
                {
                    'url': default_url + '123',
                    "Endpoint": 'v1/example3',
                    'customHeaders': "{'content-type': 'application/json', 'Accept-Language': 'en'}",
                    "Optional auth type": '',
                    "auth": ''
                }
            ]
        }


class ApiSniffer:
    @staticmethod
    def get_endpoints_already_sniffed() -> list:
        """
            Endpoint to get information about Endpoints Already Sniffed

            @return list<EndpointAlreadySniffed>
        """
        return Database.select_many({}, {}, EndpointAlreadySniffed(), '', '')

    @staticmethod
    def start_sniffing(endpoint_information: list):
        """
            Method to start with the process to get information about endpoints passed from frontend
        """

        endpoints_results = {}

        for endpoint in endpoint_information:
            endpoint_url = endpoint['endpoint']
            headers = json.loads(str(endpoint['customHeaders']).replace("'", '"'))
            request = Utils.compose_request(endpoint['endpoint'], 'get', headers, {})

            if request.status_code >= 400:
                continue

            dataframe = pd.DataFrame(request.json()['data'])
            dataframe = dataframe.fillna(0)

            endpoint_dict_to_insert = {endpoint_url: dataframe.to_dict(orient='records')}

            entity = EndpointAlreadySniffed() \
                .set_endpoint(endpoint['endpoint']) \
                .set_information(endpoint_dict_to_insert)

            Database.insert(entity)

            endpoints_results[endpoint_url] = endpoint_dict_to_insert[endpoint_url]

        return endpoints_results


class SniffedEndpointInformationManager:

    def __init__(self, information):
        self.endpointInformation = pd.DataFrame(information)

    def filter_information(self, field: str, filter_value: Any, order: bool):
        filtered_information = self.endpointInformation[(field == filter_value)]
        filtered_information.sort_values(ascending=order)
