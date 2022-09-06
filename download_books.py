import argparse
import json
import os
import time
from urllib.parse import urlparse

import requests

from additional_modules import parse_book, download_image, check_for_redirect
from parse_tululu_category import parse_book_category


def download_book(book_id, book_name, book_count, folder):
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


def fetch_book(book_url, book_count, dest_folder, skip_imgs, skip_txt):
    response = requests.get(book_url, allow_redirects=True)
    response.raise_for_status()

    check_for_redirect(response)

    folder = os.path.join(dest_folder, 'books') if dest_folder else 'books'
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

    img_scr = 'Стоит фильтр на картинку' if skip_imgs and skip_imgs in picture_name else download_image(picture_url,
                                                                                                        picture_name,
                                                                                                        dest_folder)

    book_path = 'Стоит фильтр на книгу' if skip_txt and skip_txt in book_name else download_book(number_id,
                                                                                                      book_name,
                                                                                                      book_count,
                                                                                                      folder)

    return {'title': book_name, 'author': author_name, 'img_scr': img_scr, 'book_path': book_path,
            'genres': book_genres, 'comments': book_comments}


def write_to_file(books, json_path):
    path = os.path.join(json_path, 'downloaded_books.json') if json_path else 'downloaded_books.json'
    with open(path, 'w') as file:
        json.dump(books, file, ensure_ascii=False)


def main():
    books = {}
    book_count = 0

    parser = argparse.ArgumentParser(
        description='Скачиваем книги и выводим информацию по ним'
    )
    parser.add_argument('--start_page', help='Начать с этой страницы', nargs='?', default=1, type=int)
    parser.add_argument('--end_page', help='Закончить на этой странице', nargs='?', default=1, type=int)
    parser.add_argument('--dest_folder', help='Путь к каталогу с результатами парсинга', nargs='?', default='')
    parser.add_argument('--skip_imgs', help='Не скачивать картинки', nargs='?', default='')
    parser.add_argument('--skip_txt', help='Не скачивать книги', nargs='?', default='')
    parser.add_argument('--json_path', help='Указать свой путь к *.json файлу с результатами', nargs='?', default='')
    args = parser.parse_args()

    start_page = args.start_page
    end_page = args.end_page
    dest_folder = args.dest_folder
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    json_path = args.json_path

    # start_page = 1
    # end_page = 1
    # dest_folder = ''
    # skip_imgs = ''
    # skip_txt = ''
    # json_path = ''

    if start_page > 700:
        start_page = 700
    if end_page <= start_page or end_page > 700:
        end_page = start_page

    book_urls = parse_book_category(start_page, end_page)
    for book_url in book_urls:
        book_count += 1
        try:
            downloaded_book = fetch_book(book_url, book_count, dest_folder, skip_imgs, skip_txt)
            books.update(downloaded_book)
        except requests.exceptions.HTTPError as exc:
            print("Ошибка: ", exc)
        except requests.exceptions.ConnectionError as exc:
            print("Ошибка: ", exc)
            print('Ожидаем соединение 5 минут')
            time.sleep(300)
    write_to_file(books, json_path)


if __name__ == '__main__':
    main()
