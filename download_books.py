import argparse
import os
import time

import requests

from parsing_modules import parse_book_page, download_image


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError


def download_book(id_book, folder='books/'):
    url = f'https://tululu.org/b{id_book}'
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()

    check_for_redirect(response)

    if not os.path.exists(folder):
        os.makedirs(folder)

    download_image(response)

    parsing_book = parse_book_page(response)

    author_name = parsing_book['author']
    book_name = parsing_book['title']
    book_genre = parsing_book['genre']
    book_comments = parsing_book['comments']

    path_to_file = os.path.join(folder, f'{id_book}. {book_name}.txt')
    with open(path_to_file, 'wb') as ff:
        ff.write(response.content)

    print('Название: ', book_name)
    print('Автор: ', author_name)
    print('Жанр: ', book_genre, end='\n\n')
    print('Комментарии: ', book_comments, end='\n\n')
    return path_to_file


def main():
    parser = argparse.ArgumentParser(
        description='Скачиваем книги и выводим информацию по ним'
    )
    parser.add_argument('start_id', help='Начать с этого номера книги', nargs='?', default=1, type=int)
    parser.add_argument('end_id', help='Закончить этим номером книги', nargs='?', default=2, type=int)
    args = parser.parse_args()

    start_id = args.start_id
    end_id = args.end_id

    if end_id <= start_id:
        end_id = start_id + 1

    for id_book in range(start_id, end_id):
        try:
            download_book(id_book)
        except requests.exceptions.HTTPError as exc:
            print("Ошибка: ", exc)
        except requests.exceptions.ConnectionError as exc:
            print("Ошибка: ", exc)
            print('Ожидаем соединение 5 минут')
            time.sleep(300)


if __name__ == '__main__':
    main()
