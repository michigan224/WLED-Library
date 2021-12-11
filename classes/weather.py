"""Contains the Weather class."""
import requests


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

    def __init__(self: str, zip_code: str, api_key: str):
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

    def get_lights_on(self):
        """
        Return whether or not the WLEDs is on.

        Returns
        -------
        True if the lights are on, False if not.
        """
        status = self.get_status()
        if status['error']:
            return False
        return status['on']

    def get_status(self):
        """
        Return current status of WLED lights.

        Returns
        -------
        The current state of the WLED lights.
        """
        response = requests.get(self.url)
        status = response.json()
        if response.status_code == 200:
            status['error'] = False
            return status
        status['error'] = True
        return status

    def update(self, data):
        """
        Send new state to WLED and return response.

        Parameters
        ----------
        data : dictionary
            Updated state to be passed to the lights.

        Returns
        -------
        State after the update is sent to the lights.
        """
        response = requests.post(self.url, json=data)
        status = response.json()
        if response.status_code == 200:
            status['error'] = False
            return status
        status['error'] = True
        return status
