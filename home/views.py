from django.shortcuts import render
from django.http import JsonResponse
from home.scraper import *
from .models import *
from home.tasks import add,download_image
# Create your views here.
def ru_scraper(request):
    scrape_imdb_news()
    return JsonResponse({
        "status":True,
        "message":"scraped executed"
    })

def index(request):
    a=add.delay(2,3)
    print(a)
    context={"news_data":News.objects.all()}
    return render(request,'index.html',context)