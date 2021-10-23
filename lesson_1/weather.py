# e5e4cd692a72b0b66ea0a6b80255d1c3


import requests
from pprint import pprint
import json

url = 'http://api.openweathermap.org/data/2.5/weather'

city = 'Novosibirsk'
my_params = {'q': city,
             'appid': 'e5e4cd692a72b0b66ea0a6b80255d1c3'}

response = requests.get(url, params=my_params)
j_data = response.json()
# json.(j_data
# print(type(j_data))

pprint(j_data)
print(f'В городе {j_data.get("name")} температура {round(j_data.get("main").get("temp") - 273.15, 2)} градусов')

with open('data.json', mode='w') as f:
    json.dump(j_data, fp=f)

