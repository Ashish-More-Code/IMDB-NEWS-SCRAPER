import requests
from bs4 import BeautifulSoup
from .models import *


def scrape_imdb_news():
    url='https://www.imdb.com/news/movie/'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }

    r = requests.get(url,headers=headers)
    soup=BeautifulSoup(r.text,'html.parser')
    new_items=soup.find_all('div',class_='ipc-list-card--border-line')
    for items in new_items:
        title=items.find('a',class_='ipc-link ipc-link--base')
        description=items.find('div',class_='ipc-overflowText')
        image=items.find('img',class_='ipc-image')
        external_link=title['href']
        title=title.text.strip() if title else "no title"
        description=description.text.strip() if title else "no title"
        image=image['src']
    

        news={
        "title":title,
        "description":description,
        "image":image,
        "external_link":external_link
            
        }
        News.objects.create(
            **news
        )

