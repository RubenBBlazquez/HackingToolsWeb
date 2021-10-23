from django.shortcuts import render
from django.shortcuts import render, redirect


# Create your views here.

def goToRevershellsPage(request):
    if request:
        return render(request, 'revershells_page.html')


class RevershellsAPI(APIView):

    def get(self, request):
        return JSONResponse()
        pass

    def post(self, request):

        pass
