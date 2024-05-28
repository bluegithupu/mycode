import requests
from bs4 import BeautifulSoup
import json

def scrape_douban_top250():
    url = 'https://movie.douban.com/top250'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    movie_list = []

    for page in range(0, 250, 25):
        response = requests.get(url, headers=headers, params={'start': page})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_items = soup.find_all('div', class_='item')

        for movie in movie_items:
            title = movie.find('span', class_='title').text
            rating = movie.find('span', class_='rating_num').text
            movie_list.append({'title': title, 'rating': rating})

    with open('douban_top250.json', 'w', encoding='utf-8') as f:
        json.dump(movie_list, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    scrape_douban_top250()
