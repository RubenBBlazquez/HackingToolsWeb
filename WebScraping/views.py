import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor
from time import sleep


# Create your views here.

def web_scraping_page(request):
    if request:
        return render(request, 'scraping.html', context=None)


class WebScrapingAction(APIView):
    thread_pool = ThreadPoolExecutor(20)
    module_dir = os.path.dirname(__file__)  # get current directory
    tags_data_file = module_dir + '/files/html_wordlists.json'
    webs_to_not_crawl_json = json.load(open(module_dir + '/files/webs_not_scrap.json', 'r'))
    data_crawled = []

    def get(self, request):
        return JsonResponse(json.load(open(self.tags_data_file, "r")), safe=False)

    def post(self, request):

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = requests.get(body['url'])
        compound_filter = bool(body['compoundFilter'])
        crawl_web = bool(body['crawlLinks'])

        html = BeautifulSoup(response.text, 'html.parser')
        print(body)
        data = dict()

        if not crawl_web:
            self.scrap_web(data, body, compound_filter, html)
        else:
            self.crawlWeb(data, html, body, compound_filter, [])

        self.cleanEmptyDataDict(data)

        tags_data = dict()
        tags_data['tags'] = [data]
        print(tags_data)
        return JsonResponse(tags_data, safe=False)

    # cargamos las tags enviadas por el usuario, en caso de que el usuario no haya enviado nada,
    # se cargan todas las tags disponibles de un fichero
    def scrap_web(self, data, request_data, is_compound_filter=False, html=None):

        open_file = open(self.tags_data_file, "r")
        html_tag_wordlist = {'tags': request_data['tags']} if request_data['tags'] else json.load(open_file)

        self.get_web_data(data, html_tag_wordlist, request_data, is_compound_filter, html)

    # recorre las tags y separa el tag del tipo, para saber si una tag es un atributo o una etiqueta
    # después comprueba si el usuario ha marcado que se realiza una busqueda compuesta, esto significa
    # que se buscarán tags que tengan los atributos x, sino se ha marcado buscará todo por separado
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

    # obtenemos las tags que contengan la palabra especificada
    def get_words_web_data(self, request_data, data, html):
        for word in request_data:
            self.get_tags_web_data(data, [word], html, '*:-soup-contains("{item}")', False)

    # recorremos los atributos de la request y buscamos las etiquetas que contengan ese atributo(element)
    def get_attr_web_data(self, request_data, data, element, html):

        for key in request_data.keys():
            self.get_tags_web_data(data, request_data[key], html, element + '[' + key + '*="{item}"]', True)

    # buscamos las etiquetas y las añadimos al diccionario pasado por parámetro (data_to_append)
    def get_tags_web_data(self, data_to_append=None, data_to_find=None, soup=None, select="", large_identifier=True,
                          get_only_attribute=False, attr_to_get='None'):

        if data_to_find and soup and data_to_append is not None:
            for tag in data_to_find:
                tags_list = []
                find_select = select.replace("{item}", tag)
                quotes_html = soup.select(find_select)
                for quote in quotes_html:

                    if get_only_attribute and attr_to_get in str(quote):
                        quote = quote[attr_to_get]

                    tags_list.append(str(quote))

                # con esto lo que hacemos es del parámetro de busqueda : a[class*="{item}"] cogemos la etiqueta padre
                # 'a'y luego sacar el type en este caso es una clase, pero podría ser un id, y con esto sacar el literal
                # a[class=x], para diferenciar en los resultados finales

                bracket_position = select.find("[") if select.find("[") != -1 else 0
                tag_father = select[0:bracket_position]
                type_tag = select[select.find('[') + 1:select.find('*')]

                # comprobamos que necesite un identificador largo de diferenciación(esto pasa cuando queremos sacar
                # elementos que contengan la clase x) como se ha explicado anteriormente
                if not large_identifier:
                    self.appendNewTagData(data_to_append, tag, tags_list)
                else:
                    identifier = tag_father + '[' + type_tag + '=' + tag + ']'
                    self.appendNewTagData(data_to_append, identifier, tags_list)

    # añadimos los datos al diccionario
    def appendNewTagData(self, data_dict, identifier, tags_to_append):

        if not identifier in dict(data_dict).keys():
            data_dict[identifier] = tags_to_append
        else:
            data_dict[identifier].extend(self.tagsNotAppendedYet(data_dict[identifier], tags_to_append))
            print(len(data_dict))

    def tagsNotAppendedYet(self, tags_list, tags_to_find):
        data_to_append = []

        for tag_f in tags_to_find:
            if str(tag_f).strip() not in tags_list:
                data_to_append.append(tag_f)

        return data_to_append

    # crawleamos la web, y vamos sacando todos los datos de todas las pestañas, cuando se recorre una pestaña esta se
    # elimina para no recogerla de nuevo
    def crawlWeb(self, data, soup: BeautifulSoup, request_data, compound_filter, list_pages_crawled):

        data_tags = soup.find_all('a')

        tags = {'tags': request_data['tags']}

        if len(data_tags) == 0:
            print("------------sale-----------")
            return True

        for tag in data_tags:

            if 'href' in str(tag) and tag['href'] not in list_pages_crawled \
                    and (settings.BASE_URL + tag['href']) not in list_pages_crawled \
                    and self.isUrlCrawlable(tag['href']) \
                    and self.isUrlCrawlable((settings.BASE_URL + tag['href'])):

                print(tag['href'])

                # comprobamos si la url contiene http, sino le añadimos la base url al enlace, y añadimos
                # la url a la lista de urls investigadas
                if 'http' in tag['href']:
                    response = requests.get(tag['href'])
                    list_pages_crawled.append(tag['href'])
                else:
                    response = requests.get(settings.BASE_URL + tag['href'])
                    list_pages_crawled.append(settings.BASE_URL + tag['href'])

                # sacamos los nuevos datos del nuevo enlace
                new_soup = BeautifulSoup(response.text, 'html.parser')

                del tag

                try:

                    if '404' not in new_soup.text:
                        # obtenemos los datos de la web y lo añadimos a nuestro diccionario data
                        self.get_web_data(data, tags, request_data, compound_filter, new_soup)
                        self.crawlWeb(data, new_soup, request_data, compound_filter, list_pages_crawled)

                    print(len(list_pages_crawled))

                except:
                    print("Error: unable to start thread")

    # comprueba si la url no ha sido aún vista
    def isUrlCrawlable(self, url_to_crawl):

        for url in self.webs_to_not_crawl_json['urls']:
            if url in url_to_crawl:
                return False

        return True

    # limpia posiciones sin datos en el diccionario
    def cleanEmptyDataDict(self, dictionary):
        positions_to_delete = []

        for key in dictionary.keys():
            if not dictionary[key]:
                positions_to_delete.append(key)

        for position in positions_to_delete:
            del dictionary[position]
