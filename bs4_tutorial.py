import os
import urllib.parse
from urllib.parse import urljoin, urlsplit, unquote, urlparse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def get_title_and_author(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find('h1').text.split('::')
    book_name = sanitize_filename(title.strip())
    book_author = sanitize_filename(author.strip())
    return book_name, book_author


def download_images():
    soup = BeautifulSoup(response.text, 'lxml')
    path_picture = soup.find('div', class_='bookimage').find('img')['src']
    picture_url = urljoin(url, path_picture)

    picture_unq = unquote(picture_url)
    *_, picture_name = urlsplit(picture_unq).path.split('/')

    if not os.path.exists('images'):
        os.makedirs('images')

    img_path = os.path.join('images', picture_name)
    with open(img_path, 'wb') as ff:
        ff.write(response.content)

    return img_path


def get_comments(id_book):
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        comments = ''
        for comment in soup.find_all('div', class_='texts'):
            comment_row = comment.findNext('span', class_='black').text
            comments += f'\n{comment_row}'
        if not comments:
            comments = 'Нет комментариев'
        return id_book, comments
    except AttributeError as exc:
        comments = 'Нет комментариев'
        return id_book, comments


def get_genre(id_book):
    try:
        soup = BeautifulSoup(response.text, 'lxml')
        genres = soup.find('span', class_='d_book').find_all('a')
        return [genre.text for genre in genres]
    except AttributeError:
        return "Нет книги"


def parse_book_page(response, id_book):
    title, author = get_title_and_author(response)
    genre = get_genre(id_book)
    comments = get_comments(id_book)
    image = download_images()

    print({
        'title': title,
        'author': author,
        'genre': genre,
        'comments': comments,
        'image': image,
    }
    )
    return {
        'title': title,
        'author': author,
        'genre': genre,
        'comments': comments,
        'image': image,
    }


for i in range(1, 2):
    try:
        url = f'https://tululu.org/b{i}/'
        response = requests.get(url)
        response.raise_for_status()

        parse_book_page(response, i)

    except requests.exceptions.HTTPError:
        print(i, "Нет книги")
