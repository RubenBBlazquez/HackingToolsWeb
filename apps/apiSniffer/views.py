import binascii

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from apps.apiSniffer.models import FileCreator, ApiSniffer, SniffedEndpointInformationManager
import pandas as pd
from .Enums import AuthTypesEnum
import base64


class APISnifferRedirectMethods:

    @staticmethod
    def go_to_api_sniffer_page(request):
        return render(request, 'apiSnifferPage.html')


class DefaultFileAPI(APIView):
    _fileCreator = None

    def get(self, request):
        file_type = request.GET.get('fileType')
        self._fileCreator = FileCreator()

        file_dir = self._fileCreator.get_default_file_by_type(file_type)

        response = HttpResponse(open(file_dir, 'rb'), content_type='application/octet-stream')

        return response


class GenerateEndpointsFromFile(APIView):

    @staticmethod
    def post(request):
        data = request.data
        print(data)
        dataframe = pd.DataFrame(pd.read_excel(data['endpointsFile']))
        new_endpoints = {}
        print(dataframe)

        for index, row in dataframe.iterrows():
            endpoint = row['Endpoint']
            endpoint_dict = row.fillna("").to_dict()
            auth = endpoint_dict['auth']
            auth_type = endpoint_dict['Optional auth type']

            endpoint_dict['auth'] = auth if GenerateEndpointsFromFile.valid_auth_tokens(auth_type,
                                                                                        auth) else 'not_valid'
            print(endpoint_dict)
            new_endpoints[endpoint] = endpoint_dict

        return JsonResponse(status=200, data={'message': 'success', 'data': new_endpoints}, safe=False)

    @staticmethod
    def valid_auth_tokens(auth_type, value: str) -> bool:
        if auth_type == AuthTypesEnum.BEARER.value:
            value = value.lower().replace(AuthTypesEnum.BEARER.value, '').strip()

            return value == ''

        if auth_type == AuthTypesEnum.BASIC:
            if value == '':
                return False

            try:
                value = base64.b64decode(value)

                return value != ''
            except binascii.Error:
                return False


class APISnifferAPI(APIView):
    @staticmethod
    def get(request):
        endpoint_information = ApiSniffer.get_endpoints_already_sniffed()
        print(endpoint_information)
        return JsonResponse(status=200, data=endpoint_information, safe=False)

    @staticmethod
    def post(request):
        endpoints = []
        if request.data and 'endpointsInformation' in request.data:
            endpoints = request.data['endpointsInformation']

        result_information = ApiSniffer.start_sniffing(endpoints)

        return JsonResponse(status=200, data=result_information, safe=False)


class ManageEndpointInformationAPI(APIView):

    @staticmethod
    def post(request):
        data = request.data

        if 'json' in data.keys():
            SniffedEndpointInformationManager(data)
