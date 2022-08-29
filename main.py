import os

import requests


def download_book(id, number):
    url = f'https://tululu.org/txt.php?id={id}'  # 32168
    response = requests.get(url)
    response.raise_for_status()

    if not os.path.exists('books'):
        os.makedirs('books')
    with open(f'books/{number}.txt', 'wb') as ff:
        ff.write(response.content)


if __name__ == '__main__':
    for number_book in range(1, 11):
        id_book = 32168 + number_book
        download_book(id_book, number_book)
