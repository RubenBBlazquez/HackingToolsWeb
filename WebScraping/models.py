from concurrent.futures._base import wait
from concurrent.futures.thread import ThreadPoolExecutor
import os
from enum import Enum

from bs4 import BeautifulSoup
import requests
import json
from HackingToolsWeb.settings import MySqlDB, serverCache, Utils
import time
from HackingToolsWeb.DB.Entities.TagScrapped.TagScrappedMysql import TagScrapped
from HackingToolsWeb.DB.Entities.WebScrapped.WebScrappedMysql import WebScrapped
from HackingToolsWeb.DB.Entities.LogsWebScraping.LogsWebScrapingMysql import LogsWebScraping


class WEB_SCRAPING_CACHE_KEYS(Enum):
    TAGS_SCRAPPED = 'TAGS_SCRAPPED'


class WebScraping:
    __name__ = 'Web Scraping'

    module_dir = os.path.dirname(__file__)  # get current directory

    def __init__(self, req_post_body):
        self.req_post_body = req_post_body
        self.url = req_post_body['url']
        self.is_compound_filter = bool(req_post_body['compoundFilter'])
        self.html = BeautifulSoup(requests.get(req_post_body['url']).text, 'html.parser')
        self.tags_data_file = self.module_dir + '/files/html_wordlists.json'
        self.html_tag_wordlist = {'tags': self.req_post_body['tags']} if self.req_post_body['tags'] else \
            json.load(open(self.tags_data_file, "r"))
        self.executor_crawler = ThreadPoolExecutor(max_workers=self.req_post_body['threads'])
        self.executor_get_web_data = ThreadPoolExecutor(max_workers=self.req_post_body['threads'])
        self.base_url = self.url[0: self.url.find('/', 9)]
        self.endpoints = self.url[self.url.find('/', 9):]

        MySqlDB.insert(WebScrapped().setBaseUrl(self.base_url).setEndpoint(self.endpoints))

    def scrap_web(self):
        self.get_web_data_router()

    def get_web_data_router(self):

        if self.html_tag_wordlist['tags']:
            self.get_web_data()

        if not self.is_compound_filter:
            self.get_attr_class_or_ids_web_data("")

        if self.req_post_body['word']:
            self.get_words_web_data()

    def get_web_data(self):

        """
            Recorre las tags y separa el tag del tipo, para saber si una tag es un atributo o una etiqueta
            después comprueba si el usuario ha marcado que se realiza una busqueda compuesta, esto significa
            que se buscarán tags que tengan los atributos x, sino se ha marcado buscará todo por separado

        """

        for tag in self.html_tag_wordlist['tags']:

            element = str(tag).split("-")[0].strip()
            type = str(tag).split("-")[1].strip()

            if self.is_compound_filter:
                self.get_attr_class_or_ids_web_data(element)

            else:
                if type == 'tag':
                    self.get_tags_web_data([element], element, False)

                elif type == 'attr':
                    get_only_attribute = True if element != 'id' and element != 'class' and element != 'text' else False
                    self.get_tags_web_data(elements_to_find=[element], selectQuery='[' + element + ']',
                                           large_identifier=False, get_only_attribute=get_only_attribute)

    def get_words_web_data(self):

        """
            obtenemos las tags que contengan la palabra especificada
        """

        for word in self.req_post_body['word']:
            self.get_tags_web_data(elements_to_find=[word], selectQuery='*:-soup-contains("{item}")',
                                   large_identifier=False)

    def get_attr_class_or_ids_web_data(self, element):

        """
            recorremos los atributos de la request y buscamos las etiquetas que contengan ese atributo(element)
        """

        # {'class':... , 'id':...}
        for key in self.req_post_body['attributes'].keys():
            self.get_tags_web_data(elements_to_find=self.req_post_body['attributes'][key],
                                   selectQuery=element + '[' + key + '*="{item}"]', large_identifier=True)

    def get_tags_web_data(self, elements_to_find=None, selectQuery="", large_identifier=True, get_only_attribute=False):

        """
            buscamos las etiquetas y las añadimos al atributo de la clase llamado tags_scraped

            :parameter elements_to_find -> it's a field that contains the elements (tags,attributes,words..)
                                           that we are going to find in the html

            :parameter selectQuery -> its a Optional field that contains the query we can use to find attributes or
                                      words for example `*:-soup-contains("{item}")` {item} will be replace with
                                      the elements from elements to find

            :parameter large_identifier -> its a field that define if identifier will be large ,
                                           for example if its True -> a[class=black_ops_font] and if its False -> a

            :parameter get_only_attribute -> its a boolean field to know if we must get all tag,
                                             or only the attribute that we want

        """

        if elements_to_find and self.html:

            for element in elements_to_find:
                tags_list = []

                find_select = selectQuery.replace('{item}', element)
                quotes_html = self.html.select(find_select)

                for quote in quotes_html:

                    if get_only_attribute:
                        quote = quote[element]
                        print(quote)

                    tags_list.append(str(quote))

                # comprobamos que necesite un identificador largo de diferenciación(esto pasa cuando queremos sacar
                # elementos que contengan la clase x)
                if not large_identifier:
                    self.addNewTagDataToDB(element, tags_list)
                else:
                    self.addNewTagDataToDB(self.getLargeIdentifier(soup_query=selectQuery, value=element), tags_list)

    def getLargeIdentifier(self, soup_query: str, value: str) -> str:

        """

            method to get a large identifier from a tag/attribute

            :param soup_query -> its the query that you have used to get the tags data, for example ... a[class*="{item}"]

            :param value -> its the value you have searching for example .. black_ops_font -- a[class*="black_ops_font"]

            :return str -> example. a[class=black_ops_font]

        """

        bracket_position = soup_query.find('[') if soup_query.find('[') != -1 else 0
        tag_father = soup_query[0:bracket_position]  # a
        type_tag = soup_query[soup_query.find('[') + 1:soup_query.find('*')]  # class

        return tag_father + '[' + type_tag + '=' + value + ']'

    def addNewTagDataToDB(self, identifier, tags_list):

        """
            Method to append the new data to tags scrapped

            :param identifier -> its a key to set in the tags_scrapped dictionary

            :param tags_list -> its the data to set to tags_scrapped with the identifier passed by parameter

        """

        tags_already_scrapped = serverCache.get(WEB_SCRAPING_CACHE_KEYS.TAGS_SCRAPPED.value)

        tags_not_repeated = tags_list

        if tags_already_scrapped and identifier in dict(tags_already_scrapped).keys():
            tags_not_repeated = Utils.getElementsNotRepeated(tags_already_scrapped[identifier], tags_list)
            tags_already_scrapped[identifier].extend(tags_not_repeated)
        else:
            tags_already_scrapped = tags_list

        serverCache.put(WEB_SCRAPING_CACHE_KEYS.TAGS_SCRAPPED.value, tags_already_scrapped)

        for element in tags_not_repeated:
            print('---------------------------------------------')
            print(identifier, element, self.url, self.endpoints)
            print('---------------------------------------------')
            try:
                entity = TagScrapped().setTag(identifier).setTagInfo(element).setWebScrapped(self.base_url) \
                    .setEndpointWebScrapped(self.endpoints)
                MySqlDB.insert(entity)
            except Exception as ex:
                self.insert_log(ex.args)

    def insert_log(self, message):
        MySqlDB.insert(LogsWebScraping().setLogError(message).setBaseUrl(self.base_url).setEndpoint(self.endpoints))


class CrawlWeb(WebScraping):

    def __init__(self, req_post_body):
        super(CrawlWeb, self).__init__(req_post_body)

    def crawl_web(self, soup: BeautifulSoup, threads: []):

        """
            crawleamos la web, y vamos sacando todos los datos de todas las pestañas, cuando se recorre una pestaña esta
            se elimina para no recogerla de nuevo

            :param soup:
            :param threads:

            :return:

        """
        self.get_links_to_crawl(soup, threads)
        wait(threads)

    def get_links_to_crawl(self, soup: BeautifulSoup, threads: []):

        try:

            data_tags = soup.find_all('a')

            if len(data_tags) != 0:

                for tag in data_tags:

                    if self.isUrlCrawlable(self.base_url, tag):

                        new_soup = None

                        try:
                            # comprobamos si la url contiene http, sino le añadimos la base url al enlace, y añadimos
                            # la url a la lista de urls investigadas
                            if 'http' in tag['href']:
                                response = requests.get(tag['href'])
                                serverCache.put(tag['href'], True)
                            else:
                                response = requests.get(self.base_url + tag['href'])
                                serverCache.put(self.base_url + tag['href'], True)

                            # sacamos los nuevos datos del nuevo enlace
                            new_soup = BeautifulSoup(response.text, 'html.parser')

                        except Exception as ex:
                            print('Error : to request url', ex)

                        del tag

                        try:

                            if new_soup and '404' not in new_soup.text:
                                # we set the new html beautifulSoup
                                self.html = new_soup

                                # we start to get information from the html set recently
                                threads.append(self.executor_get_web_data.submit(self.get_web_data_router))

                                # we continue crawling web
                                threads.append(self.executor_crawler.submit(self.get_links_to_crawl, new_soup, threads))

                        except Exception as ex:
                            self.insert_log(ex.args)
                            print("Error: unable to start thread -> ", ex.args)

        except Exception as ex:
            self.insert_log(ex.args)
            print('Error -- ', ex.args)

    def isUrlCrawlable(self, base_url: str, tag: {}) -> bool:
        """
            check if an url can be visited or not

            :param base_url: str
            :param tag: {}
            :return: bool

        """
        return 'href' in str(tag) and \
               serverCache.get(tag['href']) is None and serverCache.get(base_url + tag['href']) is None \
               and (base_url in tag['href'] or 'http' not in tag['href'])
