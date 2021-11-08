from dateparser import parse as parse_time
import requests
import datetime
import re
import pymongo
from abc import ABC, abstractmethod
from lxml import html
# import urllib

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}

class ConnectionMDB:
    def __init__(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        self.collection = client['news']['news']

    def add_data(self, new_row):
        if self.collection.find_one({'_id': new_row['_id']}):
            self.collection.update_one({'_id': new_row['_id']}, {'$set': new_row})
        else:
            self.collection.insert_one(new_row)

class InterfacesManager(ABC):

    @abstractmethod
    def get_data(self):
        ...

    def add_data(self, new_row: list):
        self.db_connection.add_data(new_row)

    @staticmethod
    def get_new_row():
        new_row = {
            "_id": None,  # ссылка на новость???
            "site": None,  # источник
            "header": None,  # наименование, заголовок новости
            "href": None,
            "date_of_publish": None,
        }
        return new_row

class NewsMailRu(InterfacesManager):
    def get_data(self):
        # не успел))
        ...

class LentaRu(InterfacesManager):
    def get_data(self):
        ...
        # не успел))
        # //div[contains(@class,'b-tabloid__topic_news')]
        # //div[contains(@class, 'b-tabloid__topic_news') or (contains(@class, 'item') and contains(@class, 'article'))]
        # //div[contains(@class, 'b-tabloid__topic_news') or (contains(@class, 'b-tabloid__topic') and contains(@class, 'article'))or (contains(@class, 'item') and contains(@class, 'article'))]

class YandexNews(InterfacesManager):
    def get_data(self):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}
        response = requests.get('https://yandex.ru/news/', headers=header)

        dom = html.fromstring(response.text)
        x_path = "//article[contains(@class,'mg-card')]/div[contains(@class,'mg-card__content') or contains(@class,'mg-card__text-content') or contains(@class,'mg-card__inner')]"
        items = dom.xpath(x_path)

        for item in items:

            new_row = self.get_new_row()

            new_row['href'] = item.xpath(".//@href")[0]
            new_row['_id'] = dict(re.findall(r'([^=\&]*)=([^\&]*)', new_row['href']))['persistent_id']
            new_row['site'] = 'https://yandex.ru/news/'
            new_row['header'] = item.xpath(".//div[@class='mg-card__annotation']/text()")[0]

            time_list = item.xpath("./..//span[@class='mg-card-source__time']/text()")
            time_ = time_list[0]
            if len(time_) < 6:
                time_ = 'Сегодня ' + time_

            new_row['date_of_publish'] = parse_time(u'' + time_, settings={'RELATIVE_BASE': datetime.datetime.now()})

            self.add_data(new_row)

    def __init__(self, db_connection):
        self.db_connection = db_connection


if __name__ == '__main__':
    db_connection = ConnectionMDB()

    yandex = YandexNews(db_connection)
    yandex.get_data()
