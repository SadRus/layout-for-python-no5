import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open('books_content.json', 'r') as file:
        books_json = file.read()
    books_json  = books_json.replace('/shots', 'images').replace('/images', 'images')
    books = json.loads(books_json)
    chunked_books = list(chunked(books, 2))

    rendered_page = template.render(chunked_books=chunked_books)
    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


if __name__ == '__main__':
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')