import requests

url = 'https://www.google.com'

response = requests.get(url)
response.headers.get('Content-Type')
response.text
response.content
response.content.decode('utf-8')

if response.status_code == 200:
    pass

if response.ok:
    pass

print()
