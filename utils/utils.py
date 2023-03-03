import csv
import os
import re

from bs4 import BeautifulSoup


person_dict = {
        'city': None,
        'name': None,
        'position': None,
        'e-mail': None
}


def read_file(path: str = os.path.join('temp', 'index.html')) -> str:
    """
    Возвращает содержимое обрабатываемого файла.
    :param path: путь к обрабатываемому файлу.
    :return src: содержимое файла
    """
    with open(path, 'r', encoding='utf-8') as file:
        src = file.read()
    return src


def create_new_table(path: str = os.path.join('results', 'contacts.csv')) -> None:
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(person_dict.keys())


def save_data(person: dict, path: str = os.path.join('results', 'contacts.csv')):
    with open(path, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(person.values())


def del_invisible_on_id(soup: BeautifulSoup, item_id: str):
    for_del = soup.find('div', {'class': re.compile(item_id)})
    for_del.decompose()