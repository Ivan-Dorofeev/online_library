from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_book_ids():
    fantastic_books_url = 'https://tululu.org/l55/'
    response = requests.get(fantastic_books_url, allow_redirects=True)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    books_link = soup.find('td', class_='ow_px_td').find_all('a')

    book_ids = []
    for book_link in books_link:
        if str(book_link['href']).startswith('/b'):
            if book_link['href'] not in book_ids:
                book_ids.append(book_link['href'])
    return book_ids


def get_book_lonks(book_ids):
    book_urls = []
    for book_id in book_ids:
        url = urljoin('https://tululu.org', book_id)
        book_urls.append(url)
    print(book_urls)
    return book_urls


def main():
    book_ids = get_book_ids()
    book_links = get_book_lonks(book_ids)
    print(book_ids)


if __name__ == '__main__':
    main()
