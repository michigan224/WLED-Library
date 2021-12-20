"""Contains the Weather class."""
import requests
from utils import handle_request


class Weather:
    """
    A class to represent a weather object.

    ...

    Attributes
    ----------
    zip_code : str
        zip code of location
    api_key : str
        key for openweathermap api
    url : str
        url for openweathermap api with zip code
        and api key

    Methods
    -------
    get_url():
        Returns the address of the wled light state.
    get_ip():
        Returns the ip address of the lights.
    get_lights_on():
        Returns whether or not the lights are on.
    get_status():
        Returns the current status of the lights.
    update(data):
        Sends new state to the lights and returns the response.
    """

    def __init__(self, zip_code: str, api_key: str) -> None:
        """
        Initialize Weather class.

        Parameters
        ----------
            zip_code : str
                zip code of location
            api_key : str
                key for openweathermap api
        """
        self.zip_code = zip_code
        self.api_key = api_key
        self.url = f"""https://api.openweathermap.org/data/2.5/weather?zip={zip_code},
                us&units=imperial&appid={api_key}"""

    def get_url(self) -> str:
        """
        Return weather api URL.

        Returns
        -------
        Address of the weather api.
        """
        return self.url

    def get_zip_code(self) -> str:
        """
        Return zip code.

        Returns
        -------
        Zip code.
        """
        return self.zip_code

    def get_weather(self) -> dict:
        """
        Return temperature information and state.

        Returns
        -------
        Dict containing temperature, status, min and max temperatures.
        """
        response = requests.get(self.url)
        temp = response['main']['temp']
        status = response['weather'][0]['main']
        data = {'temp': temp, 'status': status,
                'temp_min': response['main']['temp_min'], 'temp_max': response['main']['temp_max']}
        return data
