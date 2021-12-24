"""Main file to change and set lights."""
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
import os
import time
from datetime import datetime

from dotenv import load_dotenv  # pylint: disable=import-error

from classes.utils import weather_to_data
from classes.weather import Weather
from classes.wled import Wled

if not os.path.exists('./logs'):
    os.makedirs('./logs')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(
    filename='./logs/runtime.log', when='D', interval=1, backupCount=10, encoding='utf-8', delay=False)
formatter = Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

load_dotenv()


def main():
    """Handle loop and sleep."""
    lights = Wled(os.getenv('WLED_IP'))
    weather = Weather(os.getenv('ZIP'), os.getenv('WEATHER_KEY'))
    while True:
        weather_data = weather.get_weather()
        if weather_data:
            data = weather_to_data(weather_data)
            if data:
                lights.update(data)
        time.sleep(60)


if __name__ == '__main__':
    main()
