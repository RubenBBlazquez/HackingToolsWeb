import json
from concurrent.futures import wait
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor
from WebScraping import models
from HackingToolsWeb.settings import serverCache


# Create your views here.

def web_scraping_page(request):
    if request:
        return render(request, 'scraping.html', context=None)


class WebScrapingAction(APIView):
    thread_pool = ThreadPoolExecutor(20)
    module_dir = os.path.dirname(__file__)  # get current directory
    tags_data_file = module_dir + '/files/html_wordlists.json'
    data_crawled = []

    def get(self, request):
        return JsonResponse(json.load(open(self.tags_data_file, "r")), safe=False)

    def post(self, request):

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = requests.get(body['url'])
        crawl_web = bool(body['crawlLinks'])

        html = BeautifulSoup(response.text, 'html.parser')
        print(body)

        if not crawl_web:
            web_scraping_object = models.WebScraping(req_post_body=body)
            web_scraping_object.scrap_web()
        else:
            threads = list()
            web_scraping_object = models.CrawlWeb(req_post_body=body)
            web_scraping_object.crawl_web(html, threads)

        return JsonResponse({'message': 'success', 'code': 200}, safe=False, status=200)

    # limpia posiciones sin datos en el diccionario
    def cleanEmptyDataDict(self, dictionary):
        positions_to_delete = []

        for key in dictionary.keys():
            if not dictionary[key]:
                positions_to_delete.append(key)

        for position in positions_to_delete:
            del dictionary[position]
