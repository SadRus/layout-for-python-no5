import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def create_parser():
    parser = argparse.ArgumentParser(
        description='Rendering online library pages'
    )
    parser.add_argument(
        '-d',
        '--dest_folder',
        default='./',
        type=str,
        metavar='',
        help='path to the file with book descriptions',
    )
    parser.add_argument(
        '-c',
        '--count_cards',
        default=10,
        type=int,
        metavar='',
        help='number of book cards per page',
    )
    parser.add_argument(
        '-m',
        '--media_prefix',
        default='../media/',
        type=str,
        metavar='',
        help='media folder prefix',
    )
    parser.add_argument(
        '-s',
        '--static_prefix',
        default='../static/',
        type=str,
        metavar='',
        help='static folder prefix',
    )
    return parser


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    static_prefix = args.static_prefix
    media_prefix = args.media_prefix
    book_cards_per_page = args.count_cards
    full_path = os.path.join(args.dest_folder, 'book_descriptions.json')

    with open(full_path, 'r') as file:
        book_descriptions = json.load(file)

    os.makedirs('./pages', exist_ok=True)
    book_cards_by_page = list(chunked(book_descriptions, book_cards_per_page))
    pages_total = len(book_cards_by_page)

    for page_num, book_descriptions in enumerate(book_cards_by_page, start=1):
        rendered_page = template.render(
            book_cards=book_descriptions,
            current_page_num=page_num,
            pages_total=pages_total,
            STATIC_PREFIX=static_prefix,
            MEDIA_PREFIX=media_prefix,
            )
        with open(f'pages/index{page_num}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
