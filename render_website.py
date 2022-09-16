import json
import os.path

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
        json_books = json.load(file)

    os.makedirs('docs', exist_ok=True)

    books_on_page = 10
    books_part = list(chunked(json_books, books_on_page))
    pages_numbers = list(range(1, len(books_part) + 1))

    for page_number, ten_books in enumerate(books_part, 1):
        books_in_row = list(chunked(ten_books, 2))
        rendered_page = template.render(books=books_in_row, pages=pages_numbers, current_page=page_number,
                                        last_page=len(books_part))
        path = os.path.join('docs', f'index{page_number}.html')
        with open(path, 'w', encoding="utf8") as file:
            file.write(rendered_page)
    return "Site rebuilt"


def main():
    print(rebuild())
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='/home/axxel/PycharmProjects/Devman/online_library')


if __name__ == '__main__':
    main()
