import os
import requests
from parsing_modules import check_for_redirect


def download_image(picture_url, picture_name, dest_folder):
    img_response = requests.get(picture_url, allow_redirects=True)
    img_response.raise_for_status()
    check_for_redirect(img_response)

    folder = os.path.join(dest_folder, 'images') if dest_folder else 'images'
    if not os.path.exists(folder):
        os.makedirs(folder)

    img_path = os.path.join(folder, picture_name)
    with open(img_path, 'wb') as img_file:
        img_file.write(img_response.content)

    return img_path


def download_book(book_id, book_name, book_count, folder):
    download_book_url = f'https://tululu.org/txt.php'
    uploads = {
        'id': {book_id}
    }
    response = requests.get(download_book_url, params=uploads, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)

    path_to_file = os.path.join(folder, f'{book_count}. {book_name}.txt')
    with open(path_to_file, 'w') as book_file:
        book_file.write(response.text)
    return path_to_file
