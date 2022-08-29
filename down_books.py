import os

import requests


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_book(id, number):
    url = f'https://tululu.org/txt.php?id={id}'  # 32168
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()

    check_for_redirect(response)

    if not os.path.exists('books'):
        os.makedirs('books')
    with open(f'books/{number}.txt', 'wb') as ff:
        ff.write(response.content)


def main():
    for number_book in range(1, 11):
        id_book = 32168 + number_book
        try:
            download_book(id_book, number_book)
        except requests.exceptions.HTTPError:
            continue


if __name__ == '__main__':
    main()
