from django.shortcuts import render, HttpResponse


def home(request):
    return render(request, template_name='home.html')
