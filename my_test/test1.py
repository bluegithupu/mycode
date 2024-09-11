import requests
from bs4 import BeautifulSoup
import json

def fetch_douban_top250():
    url = 'https://movie.douban.com/top250'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = []
    for item in soup.find_all('div', class_='item'):
        title = item.find('span', class_='title').text
        rating = item.find('span', class_='rating_num').text
        movies.append({'title': title, 'rating': rating})

    with open('top250.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)