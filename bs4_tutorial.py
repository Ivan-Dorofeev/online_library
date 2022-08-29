import os
from pathvalidate import sanitize_filename
import requests
from bs4 import BeautifulSoup

from down_books import check_for_redirect


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    if response.history:
        raise requests.exceptions.HTTPError

    if not os.path.exists(folder):
        os.makedirs(folder)

    file_name = sanitize_filename(filename)
    path_to_file = os.path.join(folder, f'{file_name}.txt')
    with open(path_to_file, 'wb') as ff:
        ff.write(response.content)

    return path_to_file


url = 'https://tululu.org/b1/'

# url = 'https://tululu.org/b1/'
# response = requests.get(url)
# response.raise_for_status()
# soup = BeautifulSoup(response.text, 'lxml')
# title, author = soup.find('h1').text.split('::')
# print(title)
# print(author.strip())
