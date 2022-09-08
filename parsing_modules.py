import time
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError


def get_title_and_author(soup):
    title, author = soup.select_one('h1').text.split('::')
    book_name = sanitize_filename(title.strip())
    book_author = sanitize_filename(author.strip())
    return book_name, book_author


def parsing_picture_name_and_url(response, soup):
    picture_path = soup.select_one('.bookimage').find('img')['src']
    picture_url = urljoin(response.url, picture_path)
    picture_unq = unquote(picture_url)
    *_, picture_name = urlsplit(picture_unq).path.split('/')
    return picture_name, picture_unq


def get_comments(soup):
    comments = ''
    pars_comments = soup.select('div.text')
    for comment in pars_comments:
        comment_row = comment.findNext('span', class_='black').text
        comments += f'\n{comment_row}'
    if not comments:
        comments = 'Нет комментариев'
    return comments


def get_genres(soup):
    genres = soup.select_one('span.d_book a')
    genres_text = ','.join([genre.text for genre in genres])
    return genres_text


def parse_book(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title, author = get_title_and_author(soup)
    try:
        genres = get_genres(soup)
    except AttributeError:
        genres = 'Нет комментариев'

    try:
        comments = get_comments(soup)
    except AttributeError:
        comments = "Нет жанра"

    picture_name, picture_url = parsing_picture_name_and_url(response, soup)

    return {
        'title': title,
        'author': author,
        'genres': genres,
        'comments': comments,
        'picture_name': picture_name,
        'picture_url': picture_url
    }


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
    check_for_redirect(response)

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
