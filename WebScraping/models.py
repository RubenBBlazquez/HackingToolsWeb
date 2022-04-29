from concurrent.futures.thread import ThreadPoolExecutor
import os
from bs4 import BeautifulSoup
import requests
import json
from HackingToolsWeb.settings import mySqlBuilder
import time


class WebScraping:
    module_dir = os.path.dirname(__file__)  # get current directory

    def __init__(self, req_post_body):
        self.req_post_body = req_post_body
        self.url = req_post_body['url']
        self.tags_scrapped = {}
        self.is_compound_filter = bool(req_post_body['compoundFilter'])
        self.html = BeautifulSoup(requests.get(req_post_body['url']).text, 'html.parser')
        self.tags_data_file = self.module_dir + '/files/html_wordlists.json'
        self.html_tag_wordlist = {'tags': self.req_post_body['tags']} if self.req_post_body['tags'] else \
            json.load(open(self.tags_data_file, "r"))
        self.executor = ThreadPoolExecutor(max_workers=10)

        mySqlBuilder.insert('WEBS_SCRAPPED',
                            {'SCRAP_DATE': time.strftime('%Y-%m-%d %H:%M:%S'), 'WEB_SCRAPPED': self.url,
                             'SCRAP_FINISHED': False})

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

        tags_not_repeated = tags_list

        if identifier in dict(self.tags_scrapped).keys():
            tags_not_repeated = self.tagsNotAppendedYet(self.tags_scrapped[identifier], tags_list)
            self.tags_scrapped[identifier].extend(tags_not_repeated)
        else:
            self.tags_scrapped[identifier] = tags_list

        for element in tags_not_repeated:
            mySqlBuilder.insert('TAGS_FROM_WEB_SCRAPPED',
                                {'TAG': identifier, 'TAG_INFO': element, 'WEB_SCRAPPED': self.url})

    def tagsNotAppendedYet(self, original_tag_list, new_tags) -> list:

        """
            we check if the tags of new_tags list are not already in the original list and return which are not

            :param original_tag_list -> its a list with the original elements

            :param new_tags -> its a list with new elements to add

            :return list

        """

        data_to_append = []

        for tag in new_tags:
            if str(tag).strip() not in original_tag_list:
                data_to_append.append(tag)

        return data_to_append


class CrawlWeb(WebScraping):

    def __init__(self, req_post_body):
        super(CrawlWeb, self).__init__(req_post_body)
        self.crawl_web = bool(self.req_post_body['crawlLinks'])

    def crawlWeb(self, soup: BeautifulSoup, list_pages_crawled: []):

        """
            crawleamos la web, y vamos sacando todos los datos de todas las pestañas, cuando se recorre una pestaña esta
            se elimina para no recogerla de nuevo

            :param soup:

            :param list_pages_crawled:

            :return:

        """

        base_url = self.url[0: self.url.find('/', 9)]

        data_tags = soup.find_all('a')

        if len(data_tags) == 0:
            print("------------sale-----------")
            return True

        for tag in data_tags:

            if self.isUrlCrawlable(base_url, tag, list_pages_crawled):

                print(tag['href'])
                new_soup = None

                try:
                    # comprobamos si la url contiene http, sino le añadimos la base url al enlace, y añadimos
                    # la url a la lista de urls investigadas
                    if 'http' in tag['href']:
                        response = requests.get(tag['href'], cookies={'MoodleSession': 'h9uetqqaa6dk05nf0ferlbionf'})
                        list_pages_crawled.append(tag['href'])
                    else:
                        response = requests.get(base_url + tag['href'],cookies={'MoodleSession': 'h9uetqqaa6dk05nf0ferlbionf'})
                        list_pages_crawled.append(base_url + tag['href'])

                    # sacamos los nuevos datos del nuevo enlace
                    new_soup = BeautifulSoup(response.text, 'html.parser')

                except Exception as ex:
                    print('Error : to request url', ex)

                del tag

                try:

                    if new_soup and '404' not in new_soup.text:
                        # obtenemos los datos de la web
                        self.get_web_data_router()

                        # seguimos crawleando la web
                        self.executor.submit(self.crawl_web, new_soup, list_pages_crawled)

                    print(len(list_pages_crawled))

                except:
                    print("Error: unable to start thread")

    # comprueba si la url puede ser visitada o no
    def isUrlCrawlable(self, base_url: str, tag: {}, list_pages_crawled: []):
        return 'href' in str(tag) and \
               tag['href'] not in list_pages_crawled and \
               (base_url + tag['href']) not in list_pages_crawled and \
               (base_url in tag['href'] or 'http' not in tag['href'])
