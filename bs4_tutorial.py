import os
import urllib.parse
from urllib.parse import urljoin, urlsplit, unquote, urlparse

import requests
from bs4 import BeautifulSoup


def download_images(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    path_picture = soup.find('div', class_='bookimage').find('img')['src']
    picture_url = urljoin(url, path_picture)
    print(picture_url)

    picture_unq = unquote(picture_url)
    *_, picture_name = urlsplit(picture_unq).path.split('/')
    print(picture_name)

    if not os.path.exists('images'):
        os.makedirs('images')

    file_path = os.path.join('images', picture_name)
    with open(file_path, 'wb') as ff:
        ff.write(response.content)

    for comment in soup.find_all('span', class_='black')[::-1]:
        print(comment.text)


def get_comments(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    try:
        comments = ''
        for comment in soup.find_all('div', class_='texts'):
            comment_row = comment.findNext('span', class_='black').text
            comments += f'\n{comment_row}'
        if not comments:
            comments = 'Нет комментариев'
        print(id, comments)
    except AttributeError as exc:
        comments = 'Нет комментариев'
        print(id, comments)


def get_genre(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()

    try:
        soup = BeautifulSoup(response.text, 'lxml')
        genres = soup.find('span', class_='d_book').find_all('a')
        for genre in genres:
            print(id, genre.text)
    except AttributeError:
        print(id, "Нет книги")
        

for i in range(1, 10):
    try:
        get_genre(i)
    except requests.exceptions.HTTPError:
        print(i, "Нет книги")
