"""HackingToolsWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from HomePage import views as hp
from WebScraping import views as ws
from apiSniffer import views as api_sniffer

urlpatterns = [
    url(r'^$', hp.home, name="homePage"),
    url(r'^webScraping/$', ws.web_scraping_page, name="WebScraping"),
    url(r'^scrapWebApi/$', ws.WebScrapingAction.as_view(), name="WebScraping"),
    url(r'^apiSniffer/$', api_sniffer.goToApiSnifferPage, name="apiSniffer"),
]
