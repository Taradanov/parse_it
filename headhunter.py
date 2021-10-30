from pprint import pprint
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re


class HeadHunter:

    def __init__(self, search_query):
        empty_data = np.zeros(0, dtype=[("vacancy", "str"),
                                        ("description", "str"),
                                        ("site", "str"),
                                        ("salary_min", "<i4"),
                                        ("salary_max", "i4"),
                                        ("currency", "str"),
                                        ])
        self.url = 'https://novosibirsk.hh.ru/'
        self.search_query = search_query
        self.data = pd.DataFrame(empty_data)
        self.page = 0
        self.new_row = {"vacancy": None,
                        "description": None,
                        "site": None,
                        "salary_min": None,
                        "salary_max": None,
                        "currency": None,
                        }

    def next_page(self):

        params = {'area': '4',
                  'fromSearchLine': 'true',
                  'text': self.search_query,
                  'from': 'suggest_post',
                  'items_on_page': 20,
                  'page': self.page
                  }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

        response = requests.get(self.url + 'search/vacancy', params=params, headers=headers)

        self.dom = BeautifulSoup(response.text, 'html.parser')

        self.page += 1

        return len(self.dom.find_all('div', {'class': 'vacancy-serp-item'}))

    def add_data(self, data):
        self.data = self.data.append(data, ignore_index=True)

    def show_data(self):
        pprint(self.data)

    def get_info(self, dom, tag, block, class_):
        block = dom.find(tag, {block: class_})
        if block:
            return block.text
        else:
            return None

    def collect_data(self):
        vacancy_serp = self.dom.find_all('div', {'class': 'vacancy-serp-item'})

        for child in vacancy_serp:

            new_row = self.new_row.copy()

            new_row['vacancy'] = self.get_info(child, 'a', 'class', 'bloko-link')
            new_row['description'] = self.get_info(child, 'div', 'data-qa', 'vacancy-serp__vacancy_snippet_requirement')
            # child.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            new_row['site'] = child.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).attrs.get('href')
            salary_block = child.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if salary_block:
                salary = salary_block.text
                currency_list = re.sub(r'\s+', ' ', salary).split(' ')
                new_row['currency'] = currency_list[-1]
                salary = re.sub(r'\s+', '', salary)
                numbers = re.findall('[0-9]+', salary)
                if len(numbers) == 2:
                    new_row['salary_min'] = int(numbers[0])
                    new_row['salary_max'] = int(numbers[1])
                elif 'от' in currency_list:
                    new_row['salary_min'] = int(numbers[0])
                elif 'до' in currency_list:
                    new_row['salary_max'] = int(numbers[0])

            self.add_data(new_row)

    def save_data(self):
        self.data.to_csv('Вакансии.csv')

vacancy = input('Введите вакансию ')
hh = HeadHunter(vacancy)

while hh.next_page():
    hh.collect_data()


hh.save_data()
hh.show_data()
