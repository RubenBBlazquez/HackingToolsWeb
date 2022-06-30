"""

    Performed By Ruben Barroso Blázquez

"""
import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.views import APIView
import requests
from bs4 import BeautifulSoup
import os
from apps.WebScraping import models


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

        response_information = self.get_information_by_action(
            action,
            base_url,
            tag,
            endpoint,
            limit,
            offset,
            search_value,
        )
        response_information['draw'] = draw

        return JsonResponse(response_information,safe=False,status=200)

    def get_information_by_action(self, action, base_url, tag, endpoint, limit, offset, search_value) -> dict:

        response_information = {}

        if action == 'TAGS_INFORMATION':
            tags_information = json.load(open(self.tags_data_file, "r"))
            return tags_information

        if action == 'TAGS_FROM_WEBS_SCRAPPED_INFORMATION_GROUPED':
            result = models.WebScraping.get_grouped_tag_count_from_web_scrapped(
                base_url,
                endpoint,
                limit,
                offset,
                search_value)

            total_results = models.WebScraping.get_grouped_tag_count_from_web_scrapped(
                base_url,
                endpoint,
                '',
                '',
                search_value
            )

            response_information = {
                'recordsTotal'   : len(total_results),
                'recordsFiltered': total_results,
                'data'           : result
            }

        if action == 'TAGS_FROM_WEBS_SCRAPPED_INFORMATION':
            records = models.WebScraping.get_tags_information_from_web_scrapped(
                base_url,
                endpoint,
                tag,
                limit,
                offset,
                search_value
            )

            total_records = models.WebScraping.get_tags_information_from_web_scrapped(
                base_url,
                endpoint,
                tag,
                limit='',
                offset='',
            )

            response_information = {
                'recordsTotal'   : len(total_records),
                'recordsFiltered': total_records,
                'data'           : records
            }

        if action == 'WEBS_SCRAPPED_INFORMATION':
            response_information = {'data': models.WebScraping.get_information_from_web_scrapped()}

        return response_information

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
            return models.WebScraping(req_post_body=request_body)

        return models.CrawlWeb(req_post_body=request_body)
