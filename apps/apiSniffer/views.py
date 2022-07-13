from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from apps.apiSniffer.models import FileCreator


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

