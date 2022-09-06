from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_max_pages(url):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.select('a.npage')[-1].text
    return int(pages)


def get_book_links(page):
    fantastic_books_url = 'https://tululu.org/l55/'
    response = requests.get(fantastic_books_url, allow_redirects=True)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    books_ids = soup.select('.ow_px_td a')

    book_urls = []
    for books_id in books_ids:
        if str(books_id['href']).startswith('/b'):
            url = urljoin('https://tululu.org', books_id['href'])
            if url not in book_urls:
                book_urls.append(url)
    return book_urls


def parse_book_category():
    book_urls = []
    for page in range(1, 2):
        book_urls += get_book_links(page)
    return book_urls


if __name__ == '__main__':
    parse_book_category()
