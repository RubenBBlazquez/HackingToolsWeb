"""

    Performed By Ruben Barroso Blázquez

"""
import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
import requests
from bs4 import BeautifulSoup
import os
from apps.WebScraping import models


# Create your views here.

def web_scraping_page(request):
    if request:
        return render(request, 'scraping.html')


class WebScrapingAction(APIView):
    tags_data_file = os.path.dirname(__file__) + '/files/html_wordlists.json'

    def get(self, request):

        action = request.GET.get('action')
        endpoint = request.GET.get('endpoint', '')
        base_url = request.GET.get('baseUrl', '')
        tag = request.GET.get('tag', '')
        limit = request.GET.get('length', '10')
        offset = request.GET.get('start', '0')
        search_value = request.GET.get('search[value]', '')

        if action == 'TAGS_INFORMATION':
            return JsonResponse(
                json.load(
                    open(
                        self.tags_data_file,
                        "r"
                    )),
                safe=False)

        elif action == 'TAGS_FROM_WEBS_SCRAPPED_INFORMATION_GROUPED':

            result = models.WebScraping.get_grouped_tag_count_from_web_scrapped(base_url,
                                                                                endpoint, limit, offset, search_value)
            total_results = len(models.WebScraping.get_grouped_tag_count_from_web_scrapped(base_url,
                                                                                           endpoint, '', '',
                                                                                           search_value))

            return JsonResponse({'recordsTotal': total_results, 'recordsFiltered': total_results, 'data': result,
                                 'draw'        : request.GET.get('draw', 1)},
                                status=200,
                                safe=False)

        elif action == 'TAGS_FROM_WEBS_SCRAPPED_INFORMATION':

            records = models.WebScraping.get_tags_information_from_web_scrapped(base_url,
                                                                                endpoint, tag, limit, offset,
                                                                                search_value)
            total_records = len(models.WebScraping.get_tags_information_from_web_scrapped(base_url,
                                                                                          endpoint, tag, '', '',
                                                                                          search_value))

            return JsonResponse({'recordsTotal': total_records, 'recordsFiltered': total_records, 'data': records,
                                 'draw'        : request.GET.get('draw', 1)},
                                status=200,
                                safe=False)

        elif action == 'WEBS_SCRAPPED_INFORMATION':
            return JsonResponse({'data': models.WebScraping.get_information_from_web_scrapped()},
                                status=200,
                                safe=False)

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
