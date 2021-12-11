"""Main file to change and set lights."""
import time
import os
from dotenv import load_dotenv  # pylint: disable=import-error
from classes.wled import Wled
from classes.weather import Weather

load_dotenv()


def main():
    """Handle loop and sleep."""
    lights = Wled(os.getenv('WLED_IP'))
    weather = Weather(os.getenv('ZIP'), os.getenv('WEATHER_KEY'))
    while True:
        weather_data = weather.get_weather()
        data = weather_to_data(weather_data)
        lights.update(data)
        time.sleep(60)


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
