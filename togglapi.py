import json
import requests
from requests.auth import HTTPBasicAuth


class TogglApi:
    def __init__(self, API_token):

        self.URI = 'https://api.track.toggl.com/'
        # Из документации
        # When using Basic Auth and API token, use the API token as username and string "api_token" as password.
        self.auth = HTTPBasicAuth(API_token, "api_token")
        self.response = None

    def get_user_info(self):

        response = requests.get(self.URI + 'api/v8/me', auth=self.auth)
        if response.ok:
            self.response = response
            self.dump_data('info_about_user')

    def dump_data(self, filename):

        if self.response == None:
            return

        j_data = self.response.json()
        with open(f'{filename}.json', mode='w') as f:
            json.dump(j_data, fp=f)


api_token = '97deaa2ed18d39f8a4a92ecbd2010e63'

toggl = TogglApi(api_token)
toggl.get_user_info()
