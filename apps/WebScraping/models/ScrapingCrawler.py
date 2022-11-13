from concurrent.futures._base import wait
import bs4
import requests
from HackingToolsWebCore.settings import serverCache
from apps.WebScraping.models.BaseWebScraping import WebScraping
from apps.WebScraping.models.WebScrapingDBQueries import WebScrapingQueries


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

    def get_links_to_crawl(self, soup: bs4.BeautifulSoup):
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
                        new_soup = bs4.BeautifulSoup(response, 'html.parser')

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
                        WebScrapingQueries.insert_log(ex.args)
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

