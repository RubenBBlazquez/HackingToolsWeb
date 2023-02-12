"""

    Performed By Ruben Barroso Blázquez

"""
import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from HackingToolsWebCore.settings import directory_separator
from apps.WebScraping.models.WebScrapingDBQueries import WebScrapingDBQueries
from apps.WebScraping.models.BaseWebScraping import WebScraping
from .models.QueueScriptLauncher import start_crawling_web, start_web_scraping, start_crawling_web2
import pickle


# Create your views here.

def web_scraping_page(request):
    if request:
        return render(request, 'scraping.html')


class WebScrapingActionAPI(APIView):
    tags_data_file = f'apps{directory_separator}WebScraping{directory_separator}models{directory_separator}files{directory_separator}html_wordlists.json'

    def get(self, request):
        action = request.GET.get('action')
        endpoint = request.GET.get('endpoint', '')
        base_url = request.GET.get('baseUrl', '')
        tag = request.GET.get('tag', '')
        limit = request.GET.get('length', '10')
        offset = request.GET.get('start', '0')
        search_value = request.GET.get('search[value]', '')
        draw = request.GET.get('draw')

        response_information = WebScrapingDBQueries.get_information_by_action(
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

        WebScrapingActionAPI.get_web_scraping_process(request_body=body)

        return JsonResponse({'message': 'success', 'code': 200}, safe=False, status=200)

    @staticmethod
    def get_web_scraping_process(request_body: {}):
        is_crawl_active = bool(request_body['crawlLinks'])
        file_name = f'tmp_{"scrapper" if not is_crawl_active else "crawler"}'
        file_path = f'apps{directory_separator}WebScraping{directory_separator}models{directory_separator}' \
                    f'files{directory_separator}{file_name}.pkl'

        if not is_crawl_active:
            with open(file_path, 'wb') as out_file:
                pickle.dump(WebScraping(web_information=request_body), out_file)

            return start_web_scraping.delay(request_body, file_path)

        return start_crawling_web.delay(request_body)
