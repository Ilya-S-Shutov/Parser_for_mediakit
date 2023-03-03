import re

from bs4 import BeautifulSoup
from fake_headers import Headers
import requests

import utils as u


def get_copy_websites():
    url = 'https://mediakit.iportal.ru/our-team'

    headers = Headers(browser='chrome', os='win', headers=True)
    req = requests.get(url, headers=headers.generate())

    if req.status_code == 200:
        src = req.text

        with open('temp/index.html', 'w', encoding='utf-8') as file:
            file.write(src)


def del_invisible_tags(soup: BeautifulSoup):
    del_tuple = ('3995684841599793822858', '4090665631599793822858', '3995684841599793822884', '4090665631599793822884')
    for index in del_tuple:
        u.del_invisible_on_id(soup, index)


def parse_supervisors(soup: BeautifulSoup):
    supervisors = soup.find_all('div', class_='t544__content t-valign_middle')
    for supervisor in supervisors:
        person = u.person_dict.copy()
        person['name'] = supervisor.find('div', field='title').text
        person['position'] = supervisor.find('div', field='descr').text
        person['e-mail'] = supervisor.find('a').text
        u.save_data(person)
        # print(person)


def parse_common(soup: BeautifulSoup):
    # blocks = soup.find_all(field=re.compile(r'tn_text\w+'))
    blocks = soup.find_all('div', class_=re.compile('artboard'))

    for artboard in blocks[3:-2]:
        items = artboard.find_all(attrs={'data-elem-type': "text"})

        person_left = u.person_dict.copy()
        person_right = u.person_dict.copy()

        for item in items:
            top = int(item.get('data-field-top-value'))
            left = int(item.get('data-field-left-value'))

            if left < 400:
                if 1 <= top < 10:
                    person_left['city'] = item.text
                elif 190 < top < 220:
                    person_left['name'] = item.text
                elif 230 < top < 250:
                    position = item.next_element.next_element
                    person_left['position'] = position
                    mail = position.find_next('a')
                    person_left['e-mail'] = mail.text
                    u.save_data(person_left)
                    # print(person_left)

            if left > 400:
                if 1 <= top < 10:
                    person_right['city'] = item.text
                elif 190 < top < 220:
                    person_right['name'] = item.text
                elif 230 < top < 250:
                    position = item.next_element.next_element
                    person_right['position'] = position
                    mail = position.find_next('a')
                    mail = position.find_next('a')
                    person_right['e-mail'] = mail.text
                    u.save_data(person_right)
                    # print(person_right)


def parse_dev(soup: BeautifulSoup):
    develops = soup.find_all('div', class_='t527__wrapperleft')
    for develop in develops:
        person = u.person_dict.copy()
        person['name'] = develop.find_next().text
        person['position'] = develop.find_next().find_next().text
        u.save_data(person)
        # print(person)


def main():
    get_copy_websites()

    src = u.read_file()
    soup = BeautifulSoup(src, 'lxml')
    u.create_new_table()

    del_invisible_tags(soup)

    parse_supervisors(soup)
    parse_common(soup)
    parse_dev(soup)

    print('Запись завершена!')


if __name__ == '__main__':
    main()
