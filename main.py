"""Main file to change and set lights."""
import logging
import os
import time
from datetime import datetime

from dotenv import load_dotenv  # pylint: disable=import-error

from classes.utils import weather_to_data
from classes.weather import Weather
from classes.wled import Wled

LOG_FILENAME = datetime.now().strftime('./logs/logfile_%H_%M_%S_%d_%m_%Y.log')
if not os.path.exists('./logs'):
    os.makedirs('./logs')
logging.basicConfig(level=logging.DEBUG, filename=LOG_FILENAME,
                    format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

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
                new_status = lights.update(data)
                if new_status:
                    logging.debug('Light\'s updated with data: %s', data)
        time.sleep(60)


if __name__ == '__main__':
    main()
