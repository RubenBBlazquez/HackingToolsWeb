import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from pip._vendor import requests
from rest_framework.views import APIView
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np


# Create your views here.

def WebScrapingPage(request):
    if request:
        return render(request, 'scraping.html', context=None)


class WebScrapingAction(APIView):

    def get(self, request):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = module_dir + '/files/html_wordlists.json';
        print("get method")
        return JsonResponse(json.load(open(file_path, "r")), safe=False)

    def post(self, request):

        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = module_dir + '/files/html_wordlists.json'
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = requests.get(body['url'])
        html = BeautifulSoup(response.text, 'html.parser')

        print(body)

        html_tag_wordlist = {}
        if body['tags']:
            html_tag_wordlist['tags'] = body['tags']
        else:
            html_tag_wordlist = json.load(open(file_path, "r"))

        data = dict()

        for i in html_tag_wordlist['tags']:
            quotes_html = html.find_all(i)
            tagsList = []
            for tag in quotes_html:
                tagsList.append(str(tag))

            data[i] = tagsList

        print(data)

        return JsonResponse(data, safe=False)
