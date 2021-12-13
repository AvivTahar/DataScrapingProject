import requests
from configurations import *


class CoordFetcher:
    def __init__(self, access_key):
        self.access_key = access_key

    def get_coord(self, city, country):
        response = requests.get(f'{GEO_API}forward?access_key={self.access_key}&query={city} {country}')
        res_first = response.json()['data'][0]

        return res_first['latitude'], res_first['longitude']


if __name__ == '__main__':
    cf = CoordFetcher('4306112a3088c5b22c4708e9915ccc2b')
    cf.get_coord('moscow', 'russia')
