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
        compound_filter = False
        print(body)

        html_tag_wordlist = {}
        if body['tags']:
            html_tag_wordlist['tags'] = body['tags']
        else:
            html_tag_wordlist = json.load(open(file_path, "r"))

        data = dict()

        for i in html_tag_wordlist['tags']:

            if compound_filter:

                if i != 'class':
                    self.getWebData(data, body['class'], html, i + '[class*="{item}"]', False)

                if i != 'id':
                    self.getWebData(data, body['id'], html, i + '[id*="{item}"]', False)

            else:

                self.getWebData(data, [i], html, i)

        if not compound_filter:
            self.getWebData(data, body['class'], html, '[class*="{item}"]', False)
            self.getWebData(data, body['id'], html, '[id*="{item}"]', False)

        self.cleanEmptyDataDict(data)
        tags_data = dict()
        tags_data['tags'] = [data]
        print(tags_data)
        return JsonResponse(tags_data, safe=False)

    def getWebData(self, data_to_append=None, data_to_find=None, soup=None, select="", isTag=True):

        if data_to_find and soup and data_to_append is not None:
            for tag in data_to_find:
                tags_list = []
                find_select = select.replace("{item}", tag)
                print(find_select)
                quotes_html = soup.select(find_select)

                for quote in quotes_html:
                    tags_list.append(str(quote))

                bracket_position = select.find("[") if select.find("[") != -1 else 0
                tag_father = select[0:bracket_position]
                type_tag = select[select.find('[') + 1:select.find('*')]

                if isTag:
                    data_to_append[tag] = tags_list
                else:
                    data_to_append[tag_father + '[' + type_tag + '=' + tag + ']'] = tags_list


    def cleanEmptyDataDict(self, dictionary):
        positions_to_delete = []

        for key in dictionary.keys():
            if not dictionary[key]:
                positions_to_delete.append(key)

        for position in positions_to_delete:
            del dictionary[position]
