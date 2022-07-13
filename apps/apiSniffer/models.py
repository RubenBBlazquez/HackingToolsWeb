import os.path

import pandas as pd
import numpy as np


class FileCreator:
    _dictionary = {}
    _absolute_path = os.path.abspath(os.getcwd())

    def __init__(self, dictionary=None, get_default_file=True):
        self._dictionary = FileCreator.get_default_endpoints_dictionary() if get_default_file else dictionary

    def get_xls_file(self, main_dict_key='Endpoints') -> str:
        """
            Method to transform a default dict into a excel

            :param main_dict_key: param to know for what key we have to normalize

            :return file dir
        """

        file_dir = self._absolute_path + '\\dictionary.xlsx'

        # con json_normalize transformamos un json (dict) en un dataframe,
        # y con recordPath sacamos las keys de dentro de ese array
        dataframe = pd.json_normalize(self._dictionary, record_path=main_dict_key)

        # creamos el excel
        dataframe.to_excel(file_dir)

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

        # creamos el excel
        dataframe.to_json(file_dir)

        return file_dir

    def get_default_file_by_type(self, file_type: str, main_dict_key='Endpoints') -> str:
        """

        """

        excel_types = ['excel', 'xls', 'xlsx']

        if file_type not in excel_types:
            return self.get_xls_file(main_dict_key)

        return self.get_json_file(main_dict_key)

    @staticmethod
    def get_default_endpoints_dictionary() -> dict:
        default_url = 'http://127.0.0.1:8000/'
        return {
            'Endpoints': [
                {
                    'url': default_url,
                    "Endpoint": 'v1/example',
                    "auth": "api key"
                },
                {
                    'url': default_url,
                    "Endpoint": 'v1/example2',
                    "auth": "bearer"
                },
                {
                    'url': default_url,
                    "Endpoint": 'v1/example3',
                    "auth": "basic"
                }
            ]
        }
