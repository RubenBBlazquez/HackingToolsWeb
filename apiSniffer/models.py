from django.db import models
import pandas as pd
import numpy as np


# Create your models here.

class FileCreator:
    _dictionary = {}

    def __init__(self, dictionary, default_file=None):
        if not default_file:
            self._dictionary = dictionary
        else:
            self._dictionary = self.getDefaultDictionary()

    def getXlsFile(self):
        print(pd.DataFrame(self._dictionary))

    def getJsonFile(self):
        print(pd.DataFrame(self._dictionary))

    def getDefaultDictionary(self):
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
