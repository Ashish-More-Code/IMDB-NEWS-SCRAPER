import requests
from bs4 import BeautifulSoup
from .models import *
from home.tasks import *
import uuid
import os
from .tasks import download_image

def scrape_imdb_news():
    url = 'https://www.imdb.com/news/movie/'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    news_items = soup.find_all('div', class_='ipc-list-card--border-line')
    for item in news_items:
        title_tag = item.find('a', class_='ipc-link ipc-link--base')
        description_tag = item.find('div', class_='ipc-overflowText')
        image_tag = item.find('img', class_='ipc-image')

        external_link = title_tag['href'] if title_tag else None
        title = title_tag.text.strip() if title_tag else "no title"
        description = description_tag.text.strip() if description_tag else "no description"
        image_url = image_tag['src'] if image_tag else None

        image_path = None
        if image_url:
            image_name = f"image_{uuid.uuid4()}.jpg"
            result = download_image.delay(image_url, 'downloads/', image_name)
            image_path = result.get()  # Wait for the task to complete

        news = {
            "title": title,
            "description": description,
            "image": image_path,
            "external_link": external_link
        }
        News.objects.create(**news)
