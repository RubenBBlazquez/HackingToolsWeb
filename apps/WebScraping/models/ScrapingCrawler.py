from concurrent.futures.thread import ThreadPoolExecutor

import bs4
import requests
from celery import app
from HackingToolsWebCore.settings import serverCache
from apps.WebScraping.models.BaseWebScraping import WebScraping


@app.shared_task()
def consume_urls_and_crawl_again(web_information: dict, links: list):
    crawler = CrawlWeb(web_information=web_information)

    try:
        if crawler.set_html_request_information(web_information['url'], False):
            crawler.get_links_to_crawl(links)
    except Exception as ex:
        print('error in celery consume_urls_and_crawl_again -> ', ex)


class CrawlWeb(WebScraping):
    __name__ = 'Crawl Web'

    # singleton
    _instance = None

    def __new__(cls, web_information=None, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, web_information=None):
        super().__init__(web_information)

    def crawl_web(self) -> None:
        """
            method to start crawling

        """
        links = self.html.find_all('a', {'href': True})
        self.get_links_to_crawl(links)

    def get_links_to_crawl(self, links: list):
        """
            Recursive method to get all information crawling tags <a> from a web

            :param links:
        """
        if len(links) != 0:

            for tag in links:

                if self.urlCanBeCrawled(self.base_url, tag):

                    response = self.get_url_crawled_response(tag)

                    # we get the new data from the response
                    new_soup = bs4.BeautifulSoup(response, 'html.parser')

                    if new_soup and '404' not in new_soup.text:
                        self.html = new_soup
                        self.scrap_web()  # we scrap the actual link to save information in db

                        tags = new_soup.find_all('a', {'href': True})
                        mapped_tags = list(map(lambda single_tag: {'href': single_tag['href']}, tags))
                        consume_urls_and_crawl_again.apply_async((self.web_information, mapped_tags))

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

    @staticmethod
    def urlCanBeCrawled(base_url: str, tag: {}) -> bool:
        """
            check if an url can be visited or not

            :param: base_url: str
            :param: tag: {}
            :return: bool

        """

        return serverCache.get(tag['href']) is None and serverCache.get(base_url + tag['href']) is None \
               and (base_url in tag['href'] or 'http' not in tag['href']) and tag['href'] != ''
