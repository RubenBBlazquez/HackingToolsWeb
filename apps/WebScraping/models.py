"""

    Performed By Ruben Barroso Blázquez

"""

from concurrent.futures._base import wait
from concurrent.futures.thread import ThreadPoolExecutor
import os
from enum import Enum

import bs4
from bs4 import BeautifulSoup
import requests
import json
from HackingToolsWebCore.settings import Database, serverCache, Utils
import time
from HackingToolsWebCore.DB.Entities.TagScrapped.TagScrappedMysql import TagScrapped
from HackingToolsWebCore.DB.Entities.TagScrapped.GroupedTagsScrappedMysql import GroupedTagsScrapped
from HackingToolsWebCore.DB.Entities.WebScrapped.WebScrappedMysql import WebScrapped
from HackingToolsWebCore.DB.Entities.LogsWebScraping.LogsWebScrapingMysql import LogsWebScraping


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
        self.html_tag_wordlist = {'tags': self.req_post_body['tags']} if self.req_post_body['tags'] \
            else json.load(open(self.tags_data_file, "r"))
        self.executor_crawler = ThreadPoolExecutor(max_workers=self.req_post_body['threads'])
        self.executor_get_web_data = ThreadPoolExecutor(max_workers=self.req_post_body['threads'])
        self.threads = []
        self.base_url = self.url[0: self.url.find('/', 9)]
        self.endpoints = self.url[self.url.find('/', 9):]

        serverCache.clear_cache()

        Database.insert(
            WebScrapped()
            .setBaseUrl(self.base_url)
            .setEndpoint(self.endpoints))

    def scrap_web(self):
        self.get_web_data_router()

    def get_web_data_router(self):

        if self.html_tag_wordlist['tags']:
            self.get_web_data()

        if not self.is_compound_filter:
            self.get_web_data_attrs_from_class_or_id("")

        if self.req_post_body['word']:
            self.get_words_web_data()

    def get_web_data(self):
        """
            1º Iterate tags and split the tag from type to know if the tag is an attribute or a tag
            2º we check if the user have marked that he want to perform a compose search, it means that we will
            search tags like classes or ids that contains the attribute x, if not we will search separately

        """

        for tag in self.html_tag_wordlist['tags']:
            tag = str(tag).split("-")
            element = tag[0].strip()
            tag_type = tag[1].strip()

            if self.is_compound_filter:
                self.get_web_data_attrs_from_class_or_id(element)
                continue

            if tag_type == 'tag':
                self.get_tags_from_web_data(elements_to_find=[element], selectQuery=element, large_identifier=False)
                continue

            if tag_type == 'attr':
                get_only_attribute = True if element != 'id' and element != 'class' and element != 'text' else False

                self.get_tags_from_web_data(
                    elements_to_find=[element],
                    selectQuery='[' + element + ']',
                    large_identifier=False,
                    get_only_attribute=get_only_attribute
                )

    def get_words_web_data(self) -> None:
        """
            we get the tags that contains the specific word
        """

        for word in self.req_post_body['word']:
            self.get_tags_from_web_data(
                elements_to_find=[word],
                selectQuery='*:-soup-contains("{item}")',
                large_identifier=False)

    def get_web_data_attrs_from_class_or_id(self, element) -> None:
        """
            we get the attributes from the request and we search tags that contains the tag passed by
            parameter

            :param element: str (html class or html id)
            :return void:
        """

        # {'class':... , 'id':...}
        for key in self.req_post_body['attributes'].keys():
            self.get_tags_from_web_data(elements_to_find=self.req_post_body['attributes'][key],
                                        selectQuery=element + '[' + key + '*="{item}"]')

    def get_tags_from_web_data(self, elements_to_find=None, selectQuery="", large_identifier=True,
                               get_only_attribute=False) -> None:
        """
            method to search tags and add to database

            :parameter elements_to_find -> it's a field that contains the elements (tags,attributes,words..)
                                           that we are going to find in the html

            :parameter selectQuery -> it's a Optional field that contains the query we can use to find attributes or
                                      words for example `*:-soup-contains("{item}")` {item} will be replace with
                                      the elements from elements to find

            :parameter large_identifier -> it's a field that define if identifier must be large ,
                                           for example if its True -> a[class=black_ops_font] and if its False -> a

            :parameter get_only_attribute -> it's a boolean field to know if we must get all tag,
                                             or only the attribute that we want like href

        """

        if elements_to_find and self.html:

            for element in elements_to_find:
                tags_list = []

                find_select = selectQuery.replace('{item}', element)
                quotes_html = self.html.select(find_select)

                for quote in quotes_html:

                    quote = self.format_href_with_url(quote)

                    if get_only_attribute:
                        quote = quote[element]

                    tags_list.append(str(quote))

                tag_identifier = WebScraping.compound_tag_identifier(large_identifier, selectQuery, element)
                self.add_new_data_to_db(tag_identifier, tags_list)

    @staticmethod
    def compound_tag_identifier(large_identifier: bool, select_query: str, element: str) -> str:
        """
            Method to compound a large identifier to a tag, that is ,

            :param large_identifier:
            :param select_query:
            :param element:
            :return: str
        """

        if large_identifier:
            return WebScraping.get_large_identifier(soup_query=select_query, value=element)

        return element

    @staticmethod
    def get_large_identifier(soup_query: str, value: str) -> str:
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

    def format_href_with_url(self, tag: bs4.element.Tag) -> bs4.element.Tag:
        """
            Method to format a tag <a> to set always the baseUrl to an endpoint

            :param tag: BeautifulSoupTag
            :return: str
        """

        if 'href' in tag.attrs and tag['href'] and 'http' not in tag['href']:
            tag['href'] = self.base_url + tag['href']

        return tag

    def add_new_data_to_db(self, identifier, tags_list) -> None:
        """
            Method to append the new data to tags scrapped

            :param identifier -> its a key to set in the tags_scrapped dictionary

            :param tags_list -> its the data to set to tags_scrapped with the identifier passed by parameter

        """

        tags_information = WebScraping.get_tags_information(identifier, tags_list)
        tags_not_repeated = tags_information['tagsNotRepeated']
        tags_already_scrapped = tags_information['tagsAlreadyScrapped']

        serverCache.put(WEB_SCRAPING_CACHE_KEYS.TAGS_SCRAPPED.value, tags_already_scrapped)

        for element in tags_not_repeated:
            try:
                entity = TagScrapped() \
                    .setTag(identifier).setTagInfo(element) \
                    .setWebScrapped(self.base_url) \
                    .setEndpointWebScrapped(self.endpoints)

                Database.insert(entity)

            except Exception as ex:
                self.insert_log(ex.args)

    @staticmethod
    def get_tags_information(identifier, tags_list) -> dict:
        """
            Method to filter tags already scrapped

            :param identifier:
            :param tags_list:
            :return: dict
        """
        tags_already_scrapped = serverCache.get(WEB_SCRAPING_CACHE_KEYS.TAGS_SCRAPPED.value)

        if tags_already_scrapped is None:
            tags_already_scrapped = {}

        if tags_already_scrapped and identifier in dict(tags_already_scrapped).keys():
            tags_not_repeated = Utils.getElementsNotRepeated(tags_already_scrapped[identifier], tags_list)
            tags_already_scrapped[identifier].extend(tags_not_repeated)

            return {'tagsNotRepeated': tags_not_repeated, 'tagsAlreadyScrapped': tags_already_scrapped}

        tags_already_scrapped[identifier] = tags_list

        return {'tagsNotRepeated': tags_list, 'tagsAlreadyScrapped': tags_already_scrapped}

    def insert_log(self, message):
        """
            Method to insert an error in DB

            :param message: error message to insert in database
        """

        Database.insert(
            LogsWebScraping()
            .setLogError(message)
            .setBaseUrl(self.base_url)
            .setEndpoint(self.endpoints))

    @staticmethod
    def get_tags_information_from_web_scrapped(
            base_url: str,
            endpoint: str,
            tag: str,
            limit: str,
            offset: str,
            search_value: str
    ) -> list:
        """

        :param base_url:
        :param endpoint:
        :param tag:
        :param limit:
        :param offset:
        :param search_value:
        :return: list
        """

        select_values = {'TAG-str', 'TAG_INFO-str', 'WEB_SCRAPPED', 'ENDPOINT_WEB_SCRAPPED-str'}

        query_values = {'WEB_SCRAPPED-str-and': base_url.strip(),
                        'ENDPOINT_WEB_SCRAPPED-str-and': endpoint.strip(),
                        'TAG-str-and': tag.strip()}

        tags = Database.select_many(select_values, query_values, TagScrapped(), limit, offset)

        return Utils.map_index_to_dict_of_lists(tags)

    @staticmethod
    def get_grouped_tag_count_from_web_scrapped(base_url: str, endpoint: str, limit: str, offset: str,
                                                search_value: str) -> list:
        """
            method to get grouped tags from webs scrapped

            :param search_value: value to find webs with a name that contains this
            :param limit: limit of values to get from db
            :param offset: start position of values
            :param base_url: from web scrapped
            :param endpoint: from web scrapped

            :return list:
        """

        select_values = {'TAG-str', 'WEB_SCRAPPED', 'ENDPOINT_WEB_SCRAPPED-str', 'COUNT(*) as COUNT-grp'}

        query_values = {
            'WEB_SCRAPPED-str-and': base_url,
            'ENDPOINT_WEB_SCRAPPED-str-and': endpoint,
            'WEB_SCRAPPED-str-or': search_value,
            'ENDPOINT_WEB_SCRAPPED-str-or': search_value,
            'TAG-str-or': search_value
        }

        tags = Database.grouped_select(select_values, query_values, GroupedTagsScrapped(), limit, offset)

        return Utils.map_index_to_dict_of_lists(tags)

    @staticmethod
    def get_information_from_web_scrapped() -> list:
        """
            method to get all webs already scrapped

            return list:
        """

        return Database.select_many(dict(), dict(), WebScrapped(), '', '')


class CrawlWeb(WebScraping):
    __name__ = 'Crawl Web'

    # singleton
    _instance = None

    def __new__(cls, req_post_body, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, req_post_body):
        super(CrawlWeb, self).__init__(req_post_body)
        self.must_stop_crawling = bool(req_post_body['stopCrawling'])

    def scrap_web(self):
        self.crawl_web(self.html)

    def crawl_web(self, soup) -> None:
        """
            method to start crawling

            :param soup:

            :return:

        """
        try:
            self.get_links_to_crawl(soup)

            if len(self.threads) > 0:
                wait(self.threads)

        except ValueError:
            print('Error to wait threads')

    def check_if_stop_crawling(self) -> bool:
        """
            Method to check if we must stop all threads

            :return: bool
        """

        print(self.must_stop_crawling and len(self.threads) > 0)
        if self.must_stop_crawling and len(self.threads) > 0:
            map(lambda thread: thread.cancel(), self.threads)
            self.executor_crawler.shutdown()
            self.executor_get_web_data.shutdown()

            if len(self.threads) > 0:
                wait(self.threads)

            return True

        return False

    def get_links_to_crawl(self, soup: BeautifulSoup):
        """
            Recursive method to get all information crawling tags <a> from a web

            :param soup:
        """

        self.check_if_stop_crawling()

        data_tags = soup.find_all('a')

        if len(data_tags) != 0:

            for tag in data_tags:

                if self.urlCanBeCrawled(self.base_url, tag):

                    new_soup = None

                    try:
                        response = self.get_url_crawled_response(tag)

                        # we get the new data from the response
                        new_soup = BeautifulSoup(response, 'html.parser')

                    except Exception as ex:
                        print('Error : to request url', ex)

                    del tag

                    try:
                        if new_soup and '404' not in new_soup.text and not self.must_stop_crawling:
                            # we set the new html beautifulSoup
                            self.html = new_soup

                            # we start to get information from the html set recently
                            self.threads.append(self.executor_get_web_data.submit(self.get_web_data_router))

                            # we continue crawling web
                            self.threads.append(self.executor_crawler.submit(self.get_links_to_crawl, new_soup))

                    except Exception as ex:
                        self.insert_log(ex.args)
                        print("Error: unable to start thread -> ", ex.args)

    def get_url_crawled_response(self, tag: bs4.element.Tag) -> str:
        """
            Method to get the url response text

            :param tag:
            :return: str
        """

        if 'http' in tag['href']:
            serverCache.put(tag['href'], True)

            return requests.get(tag['href']).text

        serverCache.put(self.base_url + tag['href'], True)

        return requests.get(self.base_url + tag['href']).text

    def urlCanBeCrawled(self, base_url: str, tag: {}) -> bool:
        """
            check if an url can be visited or not

            :param base_url: str
            :param tag: {}
            :return: bool

        """

        return not self.must_stop_crawling and 'href' in str(tag) and serverCache.get(
            tag['href']) is None and serverCache.get(base_url + tag['href']) is None \
               and (base_url in tag['href'] or 'http' not in tag['href'])
