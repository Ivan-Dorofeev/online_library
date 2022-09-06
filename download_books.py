import argparse
import json
import os
import time
from urllib.parse import urlparse

import requests

from additional_modules import parse_book, download_image, check_for_redirect
from parse_tululu_category import parse_book_category


def download_book(book_id, book_name, book_count, folder='books/'):
    download_book_url = f'https://tululu.org/txt.php'
    uploads = {
        'id': {book_id}
    }
    response = requests.get(download_book_url, params=uploads, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)

    path_to_file = os.path.join(folder, f'{book_count}. {book_name}.txt')
    with open(path_to_file, 'w') as book_file:
        book_file.write(response.text)
    return path_to_file


def fetch_book(book_url, book_count, folder='books/'):
    response = requests.get(book_url, allow_redirects=True)
    response.raise_for_status()

    check_for_redirect(response)

    if not os.path.exists(folder):
        os.makedirs(folder)

    parsed_book = parse_book(response)
    author_name = parsed_book['author']
    book_name = parsed_book['title']
    book_genres = parsed_book['genres']
    book_comments = parsed_book['comments']
    picture_name = parsed_book['picture_name']
    picture_url = parsed_book['picture_url']

    book_id = urlparse(book_url).path.split('/')[1]
    number_id = book_id[1:]

    img_scr = download_image(picture_url, picture_name)
    book_path = download_book(number_id, book_name, book_count)

    return {'title': book_name, 'author': author_name, 'img_scr': img_scr, 'book_path': book_path,
            'genres': book_genres, 'comments': book_comments}


def write_to_file(books):
    with open('downloaded_books.json', 'w') as file:
        json.dump(books, file, ensure_ascii=False)


def main():
    books = {}
    book_count = 0

    book_urls = parse_book_category()
    for book_url in book_urls:
        book_count += 1
        try:
            downloaded_book = fetch_book(book_url, book_count)
            books.update(downloaded_book)
        except requests.exceptions.HTTPError as exc:
            print("Ошибка: ", exc)
        except requests.exceptions.ConnectionError as exc:
            print("Ошибка: ", exc)
            print('Ожидаем соединение 5 минут')
            time.sleep(300)
    write_to_file(books)


if __name__ == '__main__':
    main()
