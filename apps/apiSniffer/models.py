import os.path

import pandas as pd
import numpy as np


class FileCreator:
    _dictionary = {}
    _absolute_path = os.path.abspath(os.getcwd())

    def __init__(self, dictionary=None, default_file=None):
        if not default_file:
            self._dictionary = dictionary
        else:
            self._dictionary = FileCreator.get_default_endpoints_dictionary()

    def getXlsFile(self, main_dict_key='Endpoints'):
        file_dir = self._absolute_path + '\\dictionary.xlsx'

        # con json_normalize transformamos un json (dict) en un dataframe,
        # y con recordPath sacamos las keys de dentro de ese array
        dataframe = pd.json_normalize(self._dictionary, record_path=main_dict_key)

        # creamos el excel
        dataframe.to_excel(file_dir)

        return file_dir

    def getJsonFile(self, main_dict_key='Endpoints'):
        file_dir = self._absolute_path + '\\dictionary.json'

        # con json_normalize transformamos un json (dict) en un dataframe,
        # y con recordPath sacamos las keys de dentro de ese array
        dataframe = pd.json_normalize(self._dictionary, record_path=main_dict_key)

        # creamos el excel
        dataframe.to_json(file_dir)

        return file_dir

    @staticmethod
    def get_default_endpoints_dictionary() -> dict:
        default_url = 'http://127.0.0.1/'
        return {
            'Endpoints': [
                {
                    'url'     : default_url,
                    "Endpoint": 'v1/example'
                },
                {
                    'url'     : default_url,
                    "Endpoint": 'v1/example2'
                },
                {
                    'url'     : default_url,
                    "Endpoint": 'v1/example3'
                }
            ]
        }
