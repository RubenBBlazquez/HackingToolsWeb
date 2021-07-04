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

        serie = pd.Series(index=html_tag_wordlist['tags'])
        print(serie)

        for i in html_tag_wordlist['tags']:
            quotes_html = html.find_all(i)
            tagsList = []
            for tag in quotes_html:
                tagsList.append(str(tag))

            serie[i] = tagsList

        dataframe = pd.DataFrame(serie, dtype=np.object_)
        dataframe.to_csv("data.csv", sep=",")
        array = dataframe.to_dict()
        print(array[0])
        return JsonResponse(array[0], safe=False)
