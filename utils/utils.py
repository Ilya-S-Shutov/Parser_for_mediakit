import csv
import os
import re
from typing import Dict, Union

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
    :return src: содержимое файла.
    """
    print('Открывается локальная копия...')
    with open(path, 'r', encoding='utf-8') as file:
        src = file.read()
    return src


def create_new_table(path: str = os.path.join('results', 'contacts.csv')) -> None:
    """
    Создаёт .csv файл по указанному пути. В файл будет вестись запись считанной информации.
    :param path: путь к файлу результата.
    :return: None
    """
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(person_dict.keys())


def save_data(person: Dict[str, Union[str, None]], path: str = os.path.join('results', 'contacts.csv')) -> None:
    """
    Зписывает данные об одном сотруднике в строку указанного .csv файла.
    :param person: словарь с полученной информацией о сотруднике.
    :param path: путь к файлу, в который происходит запись данных.
    :return: None
    """
    with open(path, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(person.values())


def del_invisible_on_id(soup: BeautifulSoup, item_id: str) -> None:
    """
    Удаляет указанный элемент из дерева объектов.
    :param soup: дерево объектов обрабатываемой html-страницы.
    :param item_id: идентификатор удаляемого объекта (является частью CSS селектора)
    :return: None
    """
    for_del = soup.find('div', {'class': re.compile(item_id)})
    for_del.decompose()