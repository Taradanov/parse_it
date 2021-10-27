  # https://www.kinopoisk.ru/popular/films/?   quick_filters=serials   &   tab=all
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

url = 'https://www.kinopoisk.ru'
params = {'quick_filters': 'serials',
          'tab': 'all',
          'page': 1}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

serials_list = []
while True:
    response = requests.get(url + '/popular/films/', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    serials = dom.find_all('div', {'class': 'desktop-rating-selection-film-item'})

    if response.ok and serials:
        for serial in serials:
            serial_data = {}
            info = serial.find('a', {'class': 'selection-film-item-meta__link'})
            name = info.find('p').text
            link = url + info['href']
            try:
                genre = info.find('span', {'class': 'selection-film-item-meta__meta-additional-item'}).nextSibling
                genre = genre.text
            except:
                genre = None
            rating = serial.find('span', {'class': 'rating__value'}).text
            try:
                rating = float(rating)
            except:
                rating = None

            serial_data['name'] = name
            serial_data['link'] = link
            serial_data['genre'] = genre
            serial_data['rating'] = rating
            serials_list.append(serial_data)
        print(f"Обработана {params['page']} страница")
        params['page'] += 1
    else:
        break

pprint(serials_list)

