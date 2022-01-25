import requests
import json
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


def get_api_key(key):
    config = configparser.ConfigParser()
    config.read('config.ini')  # open config.ini
    # check for opewmap project, and the api
    if key == 'openWeather':
        return config['openweathermap']['api']
    elif key == 'ipgeolocation':
        return config['ipgeolocation']['api']


def get_weather_results(zip_code, other, api_key):
    # api_url = 'http://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}'.format(
    api_url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'.format(
        zip_code, other, api_key)
    r = requests.get(api_url)
    return r.json()


def getClientDetails(api_code):
    api_url = 'https://api.ipgeolocation.io/ipgeo?apiKey={}'.format(api_code)
    r = requests.get(api_url)
    return r.json()


# s = getClientDetails('26dec3b3091c4fbdbd70484272e6184e')
# print(s['latitude'])


@app.route('/', methods=['GET', 'POST'])
def weather_dashboard():
    temp = ''
    feels_like = ''
    weather = ''
    location = ''
    country_and_city = ''
    if request.method == "POST":
        try:
            zip_code = request.form['zipcode']
            weather_api_key = get_api_key('openWeather')
            # weather_data = get_weather_results(zip_code, weather_api_key)
            geo_api_key = get_api_key('ipgeolocation')
            geo_data = getClientDetails(geo_api_key)

            longitude = geo_data['longitude']
            latitude = geo_data['latitude']
            country_and_city = geo_data['country_name'] + \
                ' - ' + geo_data['city']

            weather_data = get_weather_results(
                longitude, latitude, weather_api_key)

            temp = "{0:.2f}".format(
                weather_data['main']['temp'])  # format it to 2dp
            feels_like = "{0:.2f}".format(weather_data['main']['feels_like'])
            weather = weather_data['weather'][0]['main']
            location = weather_data['name']

        except:
            return "ZipCode not Found"

    return render_template('home.html', country_and_city=country_and_city, temp=temp, feels_like=feels_like, weather=weather, location=location)


if __name__ == '__main__':
    app.run(debug=True)


# print(get_weather_results("95129", "34bcd1ac1db9df225cc5b733bf854091"))
# print(get_weather_results("95129",  get_api_key()))
