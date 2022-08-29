import os

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    print(response.url, response.history)
    if response.history:
        raise requests.exceptions.HTTPError


def parsing_book_name(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title, *_ = soup.find('h1').text.split('::')
    book_name = sanitize_filename(title.strip())
    return book_name


def download_book(id, folder='books/'):
    url = f'https://tululu.org/b{id}'  # 32168
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()

    check_for_redirect(response)

    if not os.path.exists('books'):
        os.makedirs('books')

    if not os.path.exists(folder):
        os.makedirs(folder)

    book_name = parsing_book_name(response)
    path_to_file = os.path.join(folder, f'{id}. {book_name}.txt')
    with open(path_to_file, 'wb') as ff:
        ff.write(response.content)
    print(path_to_file)
    return path_to_file


def main():
    for id_book in range(1, 11):
        try:
            download_book(id_book)
        except requests.exceptions.HTTPError:
            continue


if __name__ == '__main__':
    main()
