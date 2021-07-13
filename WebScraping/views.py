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
            data[i] = []
            find_all = True
            if body['class']:

                for cl in body['class']:
                    print(i, '[class*="', cl, '"]')
                    tags_list = []
                    quotes_html = html.select(i + '[class*="' + cl + '"]')
                    for tag in quotes_html:
                        tags_list.append(str(tag))

                    data[i] += tags_list
                    print("-------------------", data[i])
                    find_all = False

            if body['id']:

                for id in body['id']:
                    quotes_html = html.find_all(i, attrs={"id": id})
                    for tag in quotes_html:
                        tags_list.append(str(tag))
                    data[id] = tags_list
                    find_all = False

            if find_all:
                quotes_html = html.find_all(i)

                for tag in quotes_html:
                    tags_list.append(str(tag))

                data[i] = tags_list

        print(data)



        return JsonResponse(data, safe=False)
