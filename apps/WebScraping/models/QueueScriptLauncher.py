import pickle
from celery import app
from apps.WebScraping.models.ScrapingCrawler import CrawlWeb


@app.shared_task
def start_crawling_web(web_information: dict) -> None:
    crawler = CrawlWeb(web_information=web_information)

    if crawler.set_html_request_information(web_information['url']):
        crawler.crawl_web()


def start_crawling_web2(web_information: dict) -> None:
    crawler = CrawlWeb(web_information=web_information)

    if crawler.set_html_request_information(web_information['url']):
        crawler.crawl_web()


@app.shared_task
def start_web_scraping(web_information: dict, scrapper_path: str) -> None:
    scrapper_binary = open(scrapper_path, 'rb')
    scrapper = pickle.load(scrapper_binary)

    if scrapper.set_html_request_information(web_information['url']):
        scrapper.scrap_web()
