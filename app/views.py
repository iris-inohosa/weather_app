from flask import Blueprint, render_template, request
import requests

views = Blueprint('views', __name__, url_prefix='',
                  template_folder='templates', static_folder='static')


@views.route('/')
def index():
    return render_template('index.html')


@views.route('get-current-weather/<city_id>')
def get_current_weather(city_id):
    # foreca api
    url = f"https://foreca-weather.p.rapidapi.com/current/{city_id}"
    headers = {
        "X-RapidAPI-Key": "fea3ded0c9msh3e73fe94cc634c7p164599jsn4956791f6a6a",
        "X-RapidAPI-Host": "foreca-weather.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()['current']
        print(data)
        return data
    else:
        return {'Failed': response.status_code}


@views.route('api/get-cities/')
def get_cities():
    # foreca weather api
    querystring = request.args.get('term')
    url = f"https://foreca-weather.p.rapidapi.com/location/search/{querystring}"
    # querystring = {"lang": "en", "country": "in"} # oprtional
    headers = {
        "X-RapidAPI-Key": "fea3ded0c9msh3e73fe94cc634c7p164599jsn4956791f6a6a",
        "X-RapidAPI-Host": "foreca-weather.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        locations = response.json()['locations'][:15]
        result = []
        for city in locations:
            if 'adminArea' in city.keys():
                city_label = f"{city['name']}, {city['country']}, {city['adminArea']}"
            else:
                city_label = f"{city['name']}, {city['country']}"
            city_value = city['id']
            result.append(
                {'label': city_label, 'value': city_value})
        return result
    else:
        return {'Failed': response.status_code}


@views.route('api/get-next-days-forecast/<city_id>')
def get_forecast(city_id):
    url = f"https://foreca-weather.p.rapidapi.com/forecast/daily/{city_id}"
    querystring = {"periods": "12"}
    headers = {
        "X-RapidAPI-Key": "fea3ded0c9msh3e73fe94cc634c7p164599jsn4956791f6a6a",
        "X-RapidAPI-Host": "foreca-weather.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        return {'Failed': response.status_code}
