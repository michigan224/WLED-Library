"""Contains the WLED class."""
import requests


class Wled:
    """
    A class to represent a WLED light.

    ...

    Attributes
    ----------
    wled_ip : str
        ip address of the lights
    url : str
        address of the wled light state

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

    def __init__(self, ip_address):
        """
        Initialize WLED class.

        Parameters
        ----------
            ip_address : str
                ip address of the lights
        """
        self.wled_ip = ip_address
        self.url = f"http://{self.wled_ip}/json/state"

    def get_url(self):
        """
        Return WLED URL.

        Returns
        -------
        Address of the wled light state.
        """
        return self.url

    def get_ip(self):
        """
        Return WLED IP.

        Returns
        -------
        IP address of the lights.
        """
        return self.wled_ip

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
        """Return current status of WLED lights."""
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

        If the argument 'additional' is passed, then it is appended after the main info.

        Parameters
        ----------
        additional : str, optional
            More info to be displayed (default is None)

        Returns
        -------
        None
        """
        response = requests.post(self.url, json=data)
        status = response.json()
        if response.status_code == 200:
            status['error'] = False
            return status
        status['error'] = True
        return status
