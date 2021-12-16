"""Main file to change and set lights."""
import time
import os
from dotenv import load_dotenv  # pylint: disable=import-error
from classes.wled import Wled
from classes.weather import Weather
from classes.utils import weather_to_data

load_dotenv()


def main():
    """Handle loop and sleep."""
    lights = Wled(os.getenv('WLED_IP'))
    weather = Weather(os.getenv('ZIP'), os.getenv('WEATHER_KEY'))
    while True:
        weather_data = weather.get_weather()
        if weather_data:
            data = weather_to_data(weather_data)
            lights.update(data)
        time.sleep(60)


if __name__ == '__main__':
    main()
