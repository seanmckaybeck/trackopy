import requests


class Trackobot:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._params = {'username': username, 'password': password}
        self._auth = requests.auth.HTTPBasicAuth(username, password)
        self._url = 'https://trackobot.com/'

    def one_time_auth(self):
        endpoint = '/one_time_auth.json'
        url = self._url + endpoint
        r = requests.post(url, auth=self._auth)
        return r.json()['url'] if 'error' not in r.json() else r.json()['error']

