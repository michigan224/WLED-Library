import requests
from pprint import pprint
from dotenv import load_dotenv
import time
import os

load_dotenv()


def main():
    get_weather()


def get_weather():
    # get long and lat from .env
    zip = os.getenv('ZIP')
    key = os.getenv('WEATHER_KEY')
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip},us&appid={key}"
    # response = requests.get(url)
    response = {'temp': 30, 'statys': 'sunny'}
    pprint(response)
    return response


if __name__ == '__main__':
    main()
