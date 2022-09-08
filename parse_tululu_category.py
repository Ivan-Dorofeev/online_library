import time
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
    book_url = urljoin(fantastic_books_url, str(page))
    response = requests.get(book_url, allow_redirects=False)
    response.raise_for_status()
    if response.is_redirect:
        raise requests.exceptions.HTTPError

    soup = BeautifulSoup(response.text, 'lxml')
    books_ids = soup.select('.ow_px_td a')

    book_urls = []
    for books_id in books_ids:
        if str(books_id['href']).startswith('/b'):
            url = urljoin(fantastic_books_url, books_id['href'])
            if url not in book_urls:
                book_urls.append(url)
    return book_urls


def parse_book_category(start_page, end_page):
    book_urls = []
    for page in range(start_page, end_page + 1):
        try:
            book_urls += get_book_links(page)
        except requests.exceptions.HTTPError:
            continue
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения, ожидаем 5 минут')
            time.sleep(300)
            continue
    return book_urls
