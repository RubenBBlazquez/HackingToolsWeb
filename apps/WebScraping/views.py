"""

    Performed By Ruben Barroso Blázquez

"""
import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
import os

from apps.WebScraping.models.WebScrapingDBQueries import WebScrapingQueries
from apps.WebScraping.models.BaseWebScraping import WebScraping
from apps.WebScraping.models.ScrapingCrawler import CrawlWeb


# Create your views here.

def web_scraping_page(request):
    if request:
        return render(request, 'scraping.html')


class WebScrapingActionAPI(APIView):
    tags_data_file = os.path.dirname(__file__) + '/files/html_wordlists.json'

    def get(self, request):
        action = request.GET.get('action')
        endpoint = request.GET.get('endpoint', '')
        base_url = request.GET.get('baseUrl', '')
        tag = request.GET.get('tag', '')
        limit = request.GET.get('length', '10')
        offset = request.GET.get('start', '0')
        search_value = request.GET.get('search[value]', '')
        draw = request.GET.get('draw')

        response_information = WebScrapingQueries.get_information_by_action(
            self.tags_data_file,
            action,
            base_url,
            tag,
            endpoint,
            limit,
            offset,
            search_value,
        )
        response_information['draw'] = draw

        return JsonResponse(response_information, safe=False, status=200)

    @staticmethod
    def post(request):

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        web_scraping_object = WebScrapingActionAPI.get_web_scraping_object(request_body=body)
        web_scraping_object.scrap_web()

        return JsonResponse({'message': 'success', 'code': 200}, safe=False, status=200)

    @staticmethod
    def get_web_scraping_object(request_body: {}):
        is_crawl_active = bool(request_body['crawlLinks'])

        if not is_crawl_active:
            return WebScraping(req_post_body=request_body)

        return CrawlWeb(req_post_body=request_body)
