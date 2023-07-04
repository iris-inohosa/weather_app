import requests
from flask import request


class ForecaAPIConnector:
    """ Class to interact with Foreca Weather API via RapidAPI.
    More details: https://rapidapi.com/foreca-ltd-foreca-ltd-default/api/foreca-weather/
    """

    def __init__(self):
        self.BASE_URL = 'https://foreca-weather.p.rapidapi.com'
        self.RAPID_API_KEY = 'fea3ded0c9msh3e73fe94cc634c7p164599jsn4956791f6a6a'
        self.RAPID_API_HOST = 'foreca-weather.p.rapidapi.com'
        self.headers = {
            'X-RapidAPI-Key': self.RAPID_API_KEY,
            'X-RapidAPI-Host': self.RAPID_API_HOST
        }



    def _foreca_request(self, queryurl: str, querystring: dict = None) -> requests.Response:
        """ Method to build foreca requests

        Args:
            queryurl (str): Endpoint URL.
            querystring (dict, optional): Optional parameters. Defaults to None.

        Returns:
            requests.Response: Foreca API response.
        """
        full_url = f'{self.BASE_URL}{queryurl}'
        print(full_url)
        if querystring:
            return requests.get(
                full_url, headers=self.headers, params=querystring)
        else:
            return requests.get(
                full_url, headers=self.headers)



    def get_current_weather(self, city_id: str, querystring: dict = {'tempunit': 'C', 'windunit': 'KMH'}) -> requests.Response:
        """ Get current weather values

        Args:
            city_id (str): Selected city Foreca-Id.
            querystring (dict, optional): Defaults to {'tempunit': 'C', 'windunit': 'KMH'}.

        Returns:
            requests.Response: Foreca API response. If succeed -> data['current']
        """
        # build endpoint url
        queryurl = f'/current/{city_id}'
        return self._foreca_request(
            queryurl=queryurl, querystring=querystring)



    def get_cities_autocomplete(self, searchstring:str) -> requests.Response:
        """Get list with cities for input autocomplete fucntion

        Args:
            searchstring (str): First letters or full city name

        Returns:
            requests.Response: Foreca API response. If succeed -> data['locations']
        """
        # build endpoint url
        queryurl = f'/location/search/{searchstring}'
        response = self._foreca_request(queryurl=queryurl)
        return response



    def get_next_days_forecast(self, city_id: str) -> requests.Response:
        """Get weather data for next 11 days

        Args:
            city_id (str): Selected city Foreca-Id.

        Returns:
            requests.Response: Foreca API response. If succeed -> data['forecast']
        """
        # build endpoint url
        queryurl = f'/forecast/daily/{city_id}'
        querystring = {'tempunit': 'C', 'windunit': 'KMH',
                       'periods': '12', 'dataset': 'full'}
        return self._foreca_request(queryurl=queryurl, querystring=querystring)
