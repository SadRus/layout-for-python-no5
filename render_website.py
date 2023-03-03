import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pprint import pprint


def serialize_book_json(json_file):
    json_file = json_file.replace('/shots', 'images').replace('/images', 'images')
    return json.loads(json_file)

def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open('books_content.json', 'r') as file:
        books_json = file.read()

    books = serialize_book_json(books_json)
    rendered_page = template.render(books=books)
    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


if __name__ == '__main__':
    main()