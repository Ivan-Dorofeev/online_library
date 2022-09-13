import json
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
    books = list(chunked(json_books, 2))
    pprint(books)
    print(books[0][0])
    print(books[0][1])

    rendered_page = template.render(books=books)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print("Site rebuilt")


rebuild()
server = Server()
server.watch('template.html', rebuild)
server.serve(root='/home/axxel/PycharmProjects/Devman/online_library')
