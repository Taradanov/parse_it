import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = 'http://f5com.ru/'

response = requests.get(url)

dom = BeautifulSoup(response.text, 'html.parser')

tag_a = dom.find('a')
# print(tag_a)

parent_a = tag_a.parent.parent
# pprint(parent_a)

children = parent_a.findChildren(recursive=False)
pprint(children)

# element = dom.find('p', {'id': 'clickable'})
# # pprint(element)
#
# elements = dom.find_all('p', limit=3)
# # pprint(elements)
#
# elements = dom.find_all('p', {'class': ['red', 'paragraph']})
# # pprint(elements)
#
# p3 = dom.find_all('p', {'class': 'red paragraph left'})
#
# all_p2 = dom.select('p.paragraph.red')
# pprint(all_p2)