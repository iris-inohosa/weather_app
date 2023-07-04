import requests
from flask import request


class ForecaAPIConnector:
    def __init__(self):
        self.BASE_URL = 'https://foreca-weather.p.rapidapi.com'
        self.RAPID_API_KEY = 'fea3ded0c9msh3e73fe94cc634c7p164599jsn4956791f6a6a'
        self.RAPID_API_HOST = 'foreca-weather.p.rapidapi.com'
        self.headers = {
            'X-RapidAPI-Key': self.RAPID_API_KEY,
            'X-RapidAPI-Host': self.RAPID_API_HOST
        }

    def _foreca_request(self, queryurl: str, querystring: str = None) -> requests.Response:
        full_url = f'{self.BASE_URL}{queryurl}'
        print(full_url)
        if querystring:
            return requests.get(
                full_url, headers=self.headers, params=querystring)
        else:
            return requests.get(
                full_url, headers=self.headers)

    def get_current_weather(self, city_id: str, querystring: str = {'tempunit': 'C', 'windunit': 'KMH'}) -> requests.Response:
        # get current weather data for given city by its Id
        queryurl = f'/current/{city_id}'
        # return {'current': {'val1': 'val1', etc...}}
        return self._foreca_request(
            queryurl=queryurl, querystring=querystring)

    def get_cities_autocomplete(self, searchstring) -> requests.Response:
        queryurl = f'/location/search/{searchstring}'
        response = self._foreca_request(queryurl=queryurl)
        return response

    def get_next_days_forecast(self, city_id: str) -> requests.Response:
        queryurl = f'/forecast/daily/{city_id}'
        querystring = {'tempunit': 'C', 'windunit': 'KMH',
                       'periods': '12', 'dataset': 'full'}
        return self._foreca_request(queryurl=queryurl, querystring=querystring)
