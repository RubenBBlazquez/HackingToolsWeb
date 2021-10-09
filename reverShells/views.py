from django.shortcuts import render
from django.shortcuts import render, redirect


# Create your views here.

def goToRevershellsPage(request):
    if request:
        return render(request, 'revershells_page.html')
