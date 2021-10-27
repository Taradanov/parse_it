# https://www.kinopoisk.ru/popular/films/?quick_filters=serials&tab=all
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

from lesson_2.Kinopoisk import serials_list, serial_data

url = 'https://www.kinopoisk.ru'
params = {'quick_filters':'serials',
          'tab': 'all'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

response = requests.get(url + '/popular/films/', params=params, headers=headers)
dom = bs(response.text, 'html.parser')

if response.ok:
    serials = dom.find_all('div', {'class': 'desktop-rating-selection-film-item'})
    serials_list = []
    for serial in serials:
        serial_data = {}

