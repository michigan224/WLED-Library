import requests
from pprint import pprint
from dotenv import load_dotenv
import time
import os

load_dotenv()


def main():
    weather = get_weather()
    get_wled_status()
    turn_on = {"on": "t", "v": True, "seg": [{"pal": 0}]}
    turn_on = {"v": True, "seg": [{"pal": 2}]}
    data = weather_to_data(weather)
    update_wled(data)


def get_weather():
    # get long and lat from .env
    zip = os.getenv('ZIP')
    key = os.getenv('WEATHER_KEY')
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip},us&units=imperial&appid={key}"
    response = requests.get(url)
    response = response.json()
    pprint(response)
    temp = response['main']['feels_like']
    status = response['weather'][0]['main']
    data = {'temp': temp, 'status': status}
    return data


def get_wled_status():
    ip = os.getenv('WLED_IP')
    url = f"http://{ip}/json/state"
    print(url)
    response = requests.get(url)
    state = response.json()
    # pprint(state)
    return state


def update_wled(data):
    ip = os.getenv('WLED_IP')
    url = f"http://{ip}/json/state"
    response = requests.post(url, json=data)
    state = response.json()
    # pprint(state)
    return state


def weather_to_data(weather):
    temp = weather['temp']
    status = weather['status']
    data = {}
    if status == 'sunny':
        data = {"v": True, "seg": [
            {"pal": 4, "col": [[255, 129, 0], [255, 154, 0], [255, 193, 0]]}]}
    return data


if __name__ == '__main__':
    main()
