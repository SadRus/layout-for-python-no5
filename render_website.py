import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from dotenv import load_dotenv


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    STATIC_PREFIX = os.getenv('STATIC_PREFIX', default='../static/')
    MEDIA_PREFIX = os.getenv('MEDIA_PREFIX', default='../media/')
    book_cards_per_page = int(os.getenv('BOOK_CARDS_PER_PAGE', default=10))
    file_path = os.getenv('FILEPATH', default='./')
    full_path = os.path.join(file_path, 'books_description.json')

    with open(full_path, 'r') as file:
        books_description = json.load(file)

    os.makedirs('./pages', exist_ok=True)
    book_cards_by_page = list(chunked(books_description, book_cards_per_page))
    pages_total = len(book_cards_by_page)

    for page_num, books_description in enumerate(book_cards_by_page, start=1):
        rendered_page = template.render(
            book_cards=books_description,
            current_page_num=page_num,
            pages_total=pages_total,
            STATIC_PREFIX=STATIC_PREFIX,
            MEDIA_PREFIX=MEDIA_PREFIX,
            )
        with open(f'pages/index{page_num}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


if __name__ == '__main__':
    load_dotenv()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
