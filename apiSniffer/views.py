from django.shortcuts import render
import models as md


def goToApiSnifferPage(request):
    return render(request, 'apiSnifferPage.html')

def getFileGenerated