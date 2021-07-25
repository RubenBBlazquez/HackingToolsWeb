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

def web_scraping_page(request):
    if request:
        return render(request, 'scraping.html', context=None)


class WebScrapingAction(APIView):

    def get(self, request):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = module_dir + '/files/html_wordlists.json';
        print("get method")
        return JsonResponse(json.load(open(file_path, "r")), safe=False)

    def post(self, request):

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = requests.get(body['url'])
        compound_filter = bool(body['compoundFilter'])
        html = BeautifulSoup(response.text, 'html.parser')

        data = dict()

        try:

            self.scrap_web(data, body, compound_filter, html)
            self.cleanEmptyDataDict(data)

        except Exception as err:

            print(err)

        tags_data = dict()
        tags_data['tags'] = [data]
        print(tags_data)
        return JsonResponse(tags_data, safe=False)

    def scrap_web(self, data, request_data, is_compound_filter=False, html=None):

        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = module_dir + '/files/html_wordlists.json'
        html_tag_wordlist = {'tags': request_data['tags']} if request_data['tags'] else json.load(open(file_path, "r"))

        self.get_web_data(data, html_tag_wordlist, request_data, is_compound_filter, html)

    def get_web_data(self, data, html_tag_wordlist, request_data, is_compound_filter=False, html=None):

        for i in html_tag_wordlist['tags']:

            value = str(i).split("-")[0].strip()
            type_value = str(i).split("-")[1].strip()

            if is_compound_filter:

                self.get_attr_web_data(request_data['attributes'], data, value, html)

            else:

                if type_value == 'tag':
                    self.get_tags_web_data(data, [value], html, value, False)

                elif type_value == 'attr':
                    get_only_attribute = True if value != 'id' and value != 'class' and value != 'text' else False
                    self.get_tags_web_data(data, [value], html, '[' + value + ']', False, get_only_attribute, value)

        if not is_compound_filter: self.get_attr_web_data(request_data['attributes'], data, "", html)

        if request_data['word']: self.get_words_web_data(request_data['word'], data, html)

    def get_words_web_data(self, request_data, data, html):
        for word in request_data:
            self.get_tags_web_data(data, [word], html, '*:contains("{item}")', False)

    def get_attr_web_data(self, request_data, data, element, html):

        for key in request_data.keys():
            self.get_tags_web_data(data, request_data[key], html, element + '[' + key + '*="{item}"]', True)

    def get_tags_web_data(self, data_to_append=None, data_to_find=None, soup=None, select="", large_identifier=True,
                          get_only_attribute=False, attr_to_get='None'):

        if data_to_find and soup and data_to_append is not None:

            for tag in data_to_find:
                tags_list = []
                find_select = select.replace("{item}", tag)
                print(find_select)
                quotes_html = soup.select(find_select)

                for quote in quotes_html:

                    if get_only_attribute and attr_to_get in str(quote):
                        quote = quote[attr_to_get]

                    tags_list.append(str(quote))

                bracket_position = select.find("[") if select.find("[") != -1 else 0
                tag_father = select[0:bracket_position]
                type_tag = select[select.find('[') + 1:select.find('*')]
                if not large_identifier:
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
