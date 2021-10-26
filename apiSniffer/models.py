import os.path

import pandas as pd
import numpy as np


class FileCreator:
    _dictionary = {}

    def __init__(self, dictionary={}, default_file=None):
        if not default_file:
            self._dictionary = dictionary
        else:
            self._dictionary = self.getDefaultDictionary()

    def getXlsFile(self):
        file_dir = os.path.abspath(os.getcwd()) + '/apiSniffer/files/dictionary.xlsx'
        pd.DataFrame.from_dict(self._dictionary, orient='index').to_excel(file_dir)
        return file_dir

    def getJsonFile(self):
        print(pd.DataFrame.from_dict(self._dictionary))

    def getDefaultDictionary(self) -> dict:
        return {
            "Authorizations": [
                {
                    "Basic": {
                        "Credentials": [
                            {
                                "userName": "prueba"
                            },
                            {
                                "password": "prueba"
                            }
                        ]
                    }
                },
                {
                    'Bearer': {
                        "Credentials": [
                            {
                                "token": "prueba123"
                            }
                        ]
                    }
                }
            ],
            'Endpoints': [
                {
                    "name": 'v1/example'
                },
                {
                    "name": 'v1/example2'
                },
                {
                    "name": 'v1/example3'
                }
            ]
        }
