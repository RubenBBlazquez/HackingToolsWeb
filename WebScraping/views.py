import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
import requests
from bs4 import BeautifulSoup
import os
from WebScraping import models


# Create your views here.

def web_scraping_page(request):
    if request:
        return render(request, 'scraping.html')


class WebScrapingAction(APIView):
    tags_data_file = os.path.dirname(__file__) + '/files/html_wordlists.json'

    def get(self, request):

        action = request.GET.get('action')

        if action == 'TAGS_INFORMATION':
            return JsonResponse(
                json.load(
                    open(
                        self.tags_data_file,
                        "r"
                    )),
                safe=False)

        elif action == 'WEBS_SCRAPPED_INFORMATION':
            return JsonResponse({'index': 0, 'tags': 'a', 'count': 0, 'data': 'hola'}, safe=False)

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

        return JsonResponse(
            {'message': 'success', 'code': 200}, safe=False, status=200)
