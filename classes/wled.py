"""Contains the WLED class."""
import logging

from .utils import handle_request

logger = logging.getLogger(__name__)


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

    def __init__(self, ip_address: str) -> None:
        """
        Initialize WLED class.

        Parameters
        ----------
            ip_address : str
                ip address of the lights
        """
        self.wled_ip = ip_address
        self.url = f"http://{self.wled_ip}/json/state"

    def get_url(self) -> str:
        """
        Return WLED URL.

        Returns
        -------
        Address of the wled light state.
        """
        return self.url

    def get_ip(self) -> str:
        """
        Return WLED IP.

        Returns
        -------
        IP address of the lights.
        """
        return self.wled_ip

    def get_lights_on(self) -> bool:
        """
        Return whether or not the WLEDs is on.

        Returns
        -------
        True if the lights are on, False if not.
        """
        status = self.get_status()
        if not status:
            return None
        return status['on']

    def get_status(self) -> dict:
        """
        Return current status of WLED lights.

        Returns
        -------
        The current state of the WLED lights.
        """
        return handle_request(self.url)

    def update(self, data: dict) -> dict:
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
        return handle_request(self.url, body=data)
