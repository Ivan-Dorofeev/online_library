import json
import os.path
from pprint import pprint

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open("downloaded_books.json", "r") as file:
        books_json = file.read()
    json_books = json.loads(books_json)

    if not os.path.exists('pages'):
        os.makedirs('pages')

    books_by_ten = list(chunked(json_books, 10))
    pages_count = list(range(1, len(books_by_ten) + 1))

    for page_number, ten_books in enumerate(books_by_ten, 1):
        books_by_two = list(chunked(ten_books, 2))
        rendered_page = template.render(books=books_by_two, pages=pages_count, current_page=page_number,
                                        last_page=len(books_by_ten))
        path = os.path.join('pages', f'index{page_number}.html')
        with open(path, 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print("Site rebuilt")


rebuild()
server = Server()
server.watch('template.html', rebuild)
server.serve(root='/home/axxel/PycharmProjects/Devman/online_library')
