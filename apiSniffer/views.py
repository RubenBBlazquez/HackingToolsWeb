from django.shortcuts import render
from rest_framework.views import APIView
from apiSniffer.models import FileCreator


def goToApiSnifferPage(request):
    return render(request, 'apiSnifferPage.html')


class DefaultFileAPI(APIView):
    _fileCreator = FileCreator(default_file=True)

    def get(self, request):
        self._fileCreator.getXlsFile()
