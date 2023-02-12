from concurrent.futures.thread import ThreadPoolExecutor
import os
from enum import Enum
import bs4
from bs4 import BeautifulSoup
import requests
import json
from HackingToolsWebCore.settings import Database, serverCache, Utils
from HackingToolsWebCore.DB.Entities.WebScrapped.WebScrapped import WebScrapped
from .WebScrapingDBQueries import WebScrapingDBQueries


class WEB_SCRAPING_CACHE_KEYS(Enum):
    TAGS_SCRAPPED = 'TAGS_SCRAPPED'


class WebScraping:
    __name__ = 'Web Scraping'

    module_dir = os.path.dirname(__file__)  # get current directory

    def __init__(self, web_information):
        self.html = None
        self.base_url = ""
        self.endpoints = ""
        self.web_information = web_information
        self.tags_data_file = self.module_dir + '/files/html_wordlists.json'
        self.html_tag_wordlist = {'tags': self.web_information['tags']} if 'tags' in self.web_information \
            else json.load(open(self.tags_data_file, "r"))

        serverCache.clear_cache()

    def set_html_request_information(self, web_url: str, must_set_new_soup=True):
        """
            Method to set html information from a beautiful soup object or web url
            :param must_set_new_soup:
            :param web_url:
            :return:
        """

        if must_set_new_soup:
            request_info = requests.get(web_url)

            if request_info.status_code in ['400', '404', '500']:
                return False

            self.html = BeautifulSoup(request_info.text, 'html.parser')

        self.base_url = web_url[: web_url.find('/', 9)]
        self.endpoints = web_url[web_url.find('/', 9):]

        Database.insert(
            WebScrapped()
            .setBaseUrl(self.base_url)
            .setEndpoint(self.endpoints))

        return True

    def scrap_web(self):
        self.get_web_data_router()

    def get_web_data_router(self):
        if self.html_tag_wordlist['tags']:
            self.get_web_data()

        if not bool(self.web_information['compoundFilter']):
            self.get_web_data_attrs_from_class_or_id("")

        if self.web_information['word']:
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

            if bool(self.web_information['compoundFilter']):
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

        for word in self.web_information['word']:
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
        for key in self.web_information['attributes'].keys():
            self.get_tags_from_web_data(elements_to_find=self.web_information['attributes'][key],
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

        if elements_to_find:

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
                tags_information = WebScraping.get_tags_information(tag_identifier, tags_list)
                tags_not_repeated = tags_information['tagsNotRepeated']
                tags_already_scrapped = tags_information['tagsAlreadyScrapped']

                serverCache.put(WEB_SCRAPING_CACHE_KEYS.TAGS_SCRAPPED.value, tags_already_scrapped)

                WebScrapingDBQueries.add_new_data_to_db(tags_not_repeated, tag_identifier, self.base_url,
                                                        self.endpoints)

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

    @staticmethod
    def get_tags_information(identifier: str, tags_list: list) -> dict:
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

    def format_href_with_url(self, tag: bs4.element.Tag) -> bs4.element.Tag:
        """
            Method to format a tag <a> to set always the baseUrl to an endpoint

            :param tag: BeautifulSoupTag
            :return: str
        """

        if 'href' in tag.attrs and tag['href'] and 'http' not in tag['href']:
            tag['href'] = self.base_url + tag['href']

        return tag
