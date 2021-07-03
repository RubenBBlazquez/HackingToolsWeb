
from django.shortcuts import render, redirect


# Create your views here.

def WebScrapingPage(request):
    if request:
        return render(request,'scraping.html',context=None)


class WebScrapingAction():

    def get(self,request):
        print("get method")
        return redirect('/webScraping/')

    def post(self,request):
        print("post method")
        return redirect('/webScraping/')