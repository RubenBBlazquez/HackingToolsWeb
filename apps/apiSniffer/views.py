import json

import pandas
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from apps.apiSniffer.models import FileCreator
import pandas as pd
import numpy as np

class APISnifferRedirectMethods:

    @staticmethod
    def go_to_api_sniffer_page(request):
        return render(request, 'apiSnifferPage.html')


class ManageEndpointsInformation:
    pass


class DefaultFileAPI(APIView):
    _fileCreator = None

    def get(self, request):
        file_type = request.GET.get('fileType')
        self._fileCreator = FileCreator()

        file_dir = self._fileCreator.get_default_file_by_type(file_type)

        response = HttpResponse(open(file_dir, 'rb'), content_type='application/octet-stream')

        return response


class Endpoints:

    @staticmethod
    def get_endpoints_from_file(request):
        print('hola buenas tardes')
        return render(request, 'apiSnifferPage.html')


class GenerateEndpointsFromFile(APIView):

    @staticmethod
    def post(request):
        data = request.data

        dataframe = pd.DataFrame(pd.read_excel(data['endpointsFile']))
        groups_index = dataframe.groupby(['url']).groups
        new_endpoints = {}

        for url in groups_index.keys():
            position_elements = groups_index[url]
            new_endpoints[url] = list(
                map(lambda position: pd.Series(dataframe.iloc[position]).fillna('').to_dict(), position_elements)
            )

        return JsonResponse(status=200, data={'message': 'success', 'data': new_endpoints}, safe=False)
