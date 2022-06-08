"""HackingToolsWebCore URL Configuration """

from django.conf.urls import url
from apps.HomePage import views as hp
from apps.WebScraping import views as ws
from apps.apiSniffer import views as api_sniffer

urlpatterns = [
    url(r'^$', hp.home, name="homePage"),
    url(r'^webScraping/$', ws.web_scraping_page, name="webScraping"),
    url(r'^scrapWebApi/$', ws.WebScrapingAction.as_view(), name="webScraping"),
    url(r'^apiSniffer/$', api_sniffer.goToApiSnifferPage, name="apiSniffer"),
    url(r'^getDefaultApiSnifferFile/$', api_sniffer.DefaultFileAPI.as_view(), name="getDefaultFileAPI"),
]
