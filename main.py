"""Main file to change and set lights."""
import time
import os
from pprint import pprint
import requests
from dotenv import load_dotenv  # pylint: disable=import-error

load_dotenv()


def main():
    """Main function that handles loop and sleep."""
    while True:
        if get_wled_status()['on']:
            weather = get_weather()
            data = weather_to_data(weather)
            pprint(data)
            pprint(update_wled(data))
        time.sleep(60)


def get_weather():
    """Return temperature information and state."""
    zip_code = os.getenv('ZIP')
    key = os.getenv('WEATHER_KEY')
    url = f"""https://api.openweathermap.org/data/2.5/weather?zip={zip_code},
                us&units=imperial&appid={key}"""
    response = requests.get(url).json()
    temp = response['main']['temp']
    status = response['weather'][0]['main']
    data = {'temp': temp, 'status': status,
            'temp_min': response['main']['temp_min'], 'temp_max': response['main']['temp_max']}
    return data


def get_wled_status():
    """Return current status of WLED lights."""
    wled_ip = os.getenv('WLED_IP')
    url = f"http://{wled_ip}/json/state"
    response = requests.get(url)
    state = response.json()
    return state


def update_wled(data):
    """Sends new state to WLED and return response."""
    wled_ip = os.getenv('WLED_IP')
    url = f"http://{wled_ip}/json/state"
    response = requests.post(url, json=data)
    state = response.json()
    return state


def weather_to_data(weather):
    """Return updated values based on current weather."""
    status = weather['status']
    data = {}
    percentile = (weather['temp'] - weather['temp_min']) / \
        (weather['temp_max'] - weather['temp_min'])
    if status == 'Thunderstorm':
        data = {"v": True, "seg": [
            {"pal": 7, "fx": 43, "sx": 255, "ix": 255}]}
    elif status == 'Drizzle':
        data = {"v": True, "seg": [
            {"pal": 7, "fx": 43, "sx": 255, "ix": 55}]}
    elif status == 'Rain':
        data = {"v": True, "seg": [
            {"pal": 7, "fx": 43, "sx": 255, "ix": 120}]}
    elif status == 'Snow':
        data = {"v": True, "seg": [
            {"pal": 36, "fx": 43, "sx": 255, "ix": 120}]}
    elif status == 'Atmosphere':
        data = {"v": True, "seg": [
            {"pal": 4, "fx": 2, "sx": 100, "ix": 110,
             "col": [[211, 224, 255], [0, 0, 77], [203, 219, 255]]}]}
    elif status == 'Clear':
        col1 = [91 + (30 * percentile), 161 + (30 * percentile),
                176 + (30 * (1 - percentile))]
        col2 = [220 + (10 * percentile), 226 + (10 * percentile),
                225 + (10 * (1 - percentile))]
        col3 = [216 + (30 * percentile), 202 + (30 * percentile),
                174 + (30 * (1 - percentile))]
        data = {"v": True, "seg": [
            {"pal": 4, "col": [col1, col2, col3]}]}
    elif status == 'Clouds':
        col1 = [221 + (20 * percentile), 231 + (10 * percentile),
                238 + (10 * (1 - percentile))]
        col2 = [57 + (10 * percentile), 107 + (10 * percentile),
                137 + (10 * (1 - percentile))]
        col3 = [32 + (30 * percentile), 37 + (30 * percentile),
                71 + (30 * (1 - percentile))]
        data = {"v": True, "seg": [
            {"pal": 4, "col": [col1, col2, col3]}]}
    return data


if __name__ == '__main__':
    main()
