import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    book_cards_per_page = 15

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open('books_content.json', 'r') as file:
        books_content = json.load(file)

    for book_content in books_content:
        if book_content['img_src'] == 'nopic.gif':
            book_content['img_src'] = os.path.join(
                '../static',
                book_content['img_src']
            )
        else:
            book_content['img_src'] = os.path.join(
                '../media/images',
                book_content['img_src']
            )

    os.makedirs('./pages', exist_ok=True)
    book_cards_by_page = list(chunked(books_content, book_cards_per_page))
    pages_total = len(book_cards_by_page)

    for page_num, books_content in enumerate(book_cards_by_page, start=1):
        rendered_page = template.render(
            book_cards=books_content,
            current_page_num=page_num,
            pages_total=pages_total,
            )
        with open(f'pages/index{page_num}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


if __name__ == '__main__':
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
