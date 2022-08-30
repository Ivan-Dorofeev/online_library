import os
from urllib.parse import urljoin, urlsplit, unquote
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def get_title_and_author(soup):
    title, author = soup.find('h1').text.split('::')
    book_name = sanitize_filename(title.strip())
    book_author = sanitize_filename(author.strip())
    return book_name, book_author


def parsing_picture_name(response):
    soup = BeautifulSoup(response.text, 'lxml')
    path_picture = soup.find('div', class_='bookimage').find('img')['src']
    picture_url = urljoin(response.url, path_picture)
    picture_unq = unquote(picture_url)
    *_, picture_name = urlsplit(picture_unq).path.split('/')
    return picture_name


def download_image(response):
    picture_name = parsing_picture_name(response)

    if not os.path.exists('images'):
        os.makedirs('images')

    img_path = os.path.join('images', picture_name)
    with open(img_path, 'wb') as ff:
        ff.write(response.content)

    return img_path


def get_comments(soup):
    try:
        comments = ''
        for comment in soup.find_all('div', class_='texts'):
            comment_row = comment.findNext('span', class_='black').text
            comments += f'\n{comment_row}'
        if not comments:
            comments = 'Нет комментариев'
        return comments
    except AttributeError:
        comments = 'Нет комментариев'
        return comments


def get_genre(soup):
    try:
        genres = soup.find('span', class_='d_book').find_all('a')
        genre_text = ','.join([genre.text for genre in genres])
        return genre_text
    except AttributeError:
        return "Нет жанра"


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title, author = get_title_and_author(soup)
    genre = get_genre(soup)
    comments = get_comments(soup)
    return {
        'title': title,
        'author': author,
        'genre': genre,
        'comments': comments,
    }
