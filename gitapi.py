import json
from pprint import pprint

import requests


class GitAPI:

    def __init__(self, name):
        self.name = name
        self.url = f'https://api.github.com/users/{name}/repos'
        self.repos_name = []

    def get_repo(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            j_data = response.json()
            for info_about_repo in j_data:
                self.repos_name.append(info_about_repo.get('name'))

            with open(f'{self.name}.json', mode='w') as f:
                json.dump(j_data, fp=f)

            with open(f'{self.name}_only_names.json', mode='w') as f:
                json.dump(self.repos_name, fp=f)

        else:
            print(f'Невозможно получить список открытых репозиториев для пользователя {self.name}')

if __name__ == '__main__':

    name = input('Введите имя пользователя ')
    git_api = GitAPI(name)
    git_api.get_repo()
