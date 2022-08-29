import requests


def download_book():
    url = 'https://tululu.org/txt.php?id=32168'
    response = requests.get(url)
    response.raise_for_status()
    with open('Пески_Марса.txt', 'wb') as ff:
        ff.write(response.content)


if __name__ == '__main__':
    download_book()
