from flask import Blueprint, render_template, request, jsonify
import requests
import json
from datetime import datetime
import foreca_api
# Blueprints
# -------------------------------------------------------------------------
views = Blueprint('views', __name__, url_prefix='',
                  template_folder='templates', static_folder='static')

# -------------------------------------------------------------------------

foreca_api_connector = foreca_api.ForecaAPIConnector()

# Views
# -------------------------------------------------------------------------


@views.route('/')
def index():
    return render_template('index.html')


@views.route('api/get-current-weather/<city_id>')
def get_current_weather(city_id):
    # foreca api
    response = foreca_api_connector.get_current_weather(city_id=city_id)
    if response.status_code == 200:
        data = response.json()['current']
        return data
    else:
        return {'Failed': response.status_code}


@views.route('api/get-cities/')
def get_cities():
    # foreca weather api
    querystring = request.args.get('term')
    response = foreca_api_connector.get_cities_autocomplete(
        searchstring=querystring)
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
    response = foreca_api_connector.get_next_days_forecast(city_id=city_id)
    if response.status_code == 200:
        week_days = ['Mond', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        data = response.json()['forecast']
        for day in data:
            datetime_object = datetime.strptime(
                day['date'], '%Y-%m-%d')

            week_day = week_days[datetime_object.weekday()]
            day['weekday'] = week_day
            day['short_date'] = f'{datetime_object.day}.{datetime_object.month}'
        return {'forecast_data': data}
    else:
        return {'Failed': response.status_code}


@views.route('api/weather-forecast', methods=['GET', 'POST'])
def single_day_forecast():
    if request.method == 'POST':
        forecast_data = request.get_json()['forecast_data']
        forecast_data.pop(0)
    return jsonify({'htmlresponse': render_template('include/single_day.html', data=forecast_data)})
# -------------------------------------------------------------------------
