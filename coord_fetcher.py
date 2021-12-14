import requests
from configurations import *


class CoordFetcher:
    def __init__(self, access_key):
        self.access_key = access_key[1:-1]

    def get_coord(self, city, country):
        response = requests.get(f'{GEO_API}forward?access_key={self.access_key}&query={city} {country}')
        res_first = response.json()['data'][0]

        logging.info(f'Got API response with '
                     f'{res_first["latitude"], res_first["longitude"]}')
        return res_first['latitude'], res_first['longitude']

