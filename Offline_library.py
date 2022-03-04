import argparse
import codecs
import json
import os
from urllib.parse import urlsplit, urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathvalidate import sanitize_filename
from parse_tululu_category import parse_book_link


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError('Redirect')


def download_image(img_link, image_directory):
    response = requests.get(img_link)
    response.raise_for_status()
    image_path = urlsplit(img_link).path
    image_resolution = image_path.split('/')[-1]
    filepath = f'{image_directory}/{image_resolution}'
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_img_link(soup):
    img_selector = '.ow_px_td .d_book .bookimage img'
    img_path = soup.select_one(img_selector)['src']
    img_link = f'http://tululu.org{img_path}'
    return img_link


def parse_book_page(html_content):
    soup = BeautifulSoup(html_content.text, 'lxml')
    book_and_author_selector = '.ow_px_td h1'
    book_and_author = soup.select_one(book_and_author_selector).text
    book_splited, author_splited = book_and_author.split('::')
    book = book_splited.strip()
    author = author_splited.strip()
    genres_selector = '.ow_px_td span.d_book a'
    found_genres = soup.select(genres_selector)
    genres = [genre.text for genre in found_genres]
    comments_selector = '.ow_px_td .black'
    found_comments = soup.select(comments_selector)
    comments = [comment.text for comment in found_comments]
    img_link = get_img_link(soup)

    return {'book': book,
            'author': author,
            'genres': genres,
            'comments': comments,
            'img_link': img_link,
            }


def generate_filepath(filename, directory):
    filename = sanitize_filename(filename)
    filepath = f'{directory}/{filename}'
    return filepath


def download_book(book, book_directory, book_id):
    url = f'http://tululu.org/txt.php'
    payload = {'id': book_id }
    response = requests.get(url, params=payload, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    filename = f'{book_id}.{book}.txt'
    filepath = generate_filepath(filename, book_directory)
    with open(filepath, 'w') as file:
        file.write(response.text)


def download_json(book_directory, image_directory, book_links):
    books_info = []
    for book_link in book_links:
        html_content = requests.get(book_link)
        html_content.raise_for_status()
        book_info = parse_book_page(html_content)
        book_id = urlparse(book_link).path.strip('/')[1:]
        try:
            download_book(book_info['book'], book_directory, book_id)
            download_image(book_info['img_link'], image_directory)
            books_info.append(book_info)
        except requests.HTTPError as error:
            print(error)

    with codecs.open('all_books.json', 'w', encoding='utf8') as json_file:
        json.dump(books_info, json_file, ensure_ascii=False)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("start_id", help="Please enter the first page number", type=int)
    parser.add_argument("end_id", help="Please enter the final page number", type=int)
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id
    book_directory = os.getenv('BOOK_FOLDER')
    image_directory = os.getenv('IMAGE_FOLDER')
    os.makedirs(book_directory, exist_ok=True)
    os.makedirs(image_directory, exist_ok=True)
    for page_number in range(start_id, end_id):
        url = f'http://tululu.org/l55/{page_number}'
        html_content = requests.get(url)
        html_content.raise_for_status()
        book_links = parse_book_link(html_content)
        download_json(book_directory, image_directory, book_links)


if __name__ == '__main__':
    main()
