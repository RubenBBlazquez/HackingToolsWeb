import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from apiSniffer.models import FileCreator


def goToApiSnifferPage(request):
    return render(request, 'apiSnifferPage.html')


class DefaultFileAPI(APIView):
    _fileCreator = None

    def get(self, request):
        file_type = request.GET.get('fileType')
        self._fileCreator = FileCreator(default_file=True)
        print(file_type)
        file_dir = self._fileCreator.getXlsFile() if file_type in ['excel', 'xls', 'xlsx'] \
            else self._fileCreator.getJsonFile()

        response = HttpResponse(open(file_dir, 'rb'), content_type='application/octet-stream')

        return response

