from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from rest_framework.views import APIView


def go_to_revershell_page(request):
    if request:
        return render(request, 'revershells_page.html')


class RevershellsAPI(APIView):

    def get(self, request):
        return JsonResponse(request, 'hola', safe=False)

    def post(self, request):
        pass
