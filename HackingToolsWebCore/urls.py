"""HackingToolsWebCore URL Configuration """

from django.conf.urls import url
from apps.HomePage import views as hp
from apps.WebScraping import views as ws
from apps.apiSniffer.views import APISnifferRedirectMethods, DefaultFileAPI, GenerateEndpointsFromFile

urlpatterns = [
    url(r'^$', hp.home, name="homePage"),

    # WebScraping Page
    url(r'^webScraping/$', ws.web_scraping_page, name="webScraping"),
    url(r'^scrapWebApi/$', ws.WebScrapingActionAPI.as_view(), name="webScraping"),

    # Api Sniffer Page
    url(r'^apiSniffer/$', APISnifferRedirectMethods.go_to_api_sniffer_page, name="apiSniffer"),
    url(r'^getDefaultApiSnifferFile/$', DefaultFileAPI.as_view(), name="getDefaultFileAPI"),
    url(r'^generateEndpointsFromFile/$', GenerateEndpointsFromFile.as_view(), name="getDefaultFileAPI"),
]
