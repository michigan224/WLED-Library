"""Contains the WLED class."""
import logging
from typing import Union

from classes.utils import handle_request

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

    def __init__(self, ip_address: Union[dict, str]) -> None:
        """
        Initialize WLED class.

        Parameters
        ----------
            ip_address : dict or str
                ip address(es) of the lights
        """
        self.wled_ip = ip_address if isinstance(
            ip_address, list) else [ip_address]
        self.url = [f"http://{ip}/json/state" for ip in self.wled_ip]

    def get_url(self) -> list:
        """
        Return list of URLs for each light.

        Returns
        -------
        Address of the wled light state.
        """
        return self.url

    def get_ip(self) -> list:
        """
        Return list of IPs.

        Returns
        -------
        IP address of the lights.
        """
        return self.wled_ip

    def get_lights_on(self) -> list:
        """
        Return whether or not the WLEDs is on.

        Returns
        -------
        True if the lights are on, False if not.
        """
        status = self.get_status()
        status = [bool(state['on']) for state in status]

    def get_status(self) -> dict:
        """
        Return current status of WLED lights.

        Returns
        -------
        The current state of the WLED lights.
        """
        statuses = []
        for ip_addr in self.wled_ip:
            statuses.append(handle_request(ip_addr))
        return statuses

    def update(self, data: Union[dict, list], ip_addr=None) -> dict:
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
        if ip_addr:
            return [handle_request(f"http://{ip_addr}/json/state", data)]
        new_statuses = []
        for idx, addr in enumerate(self.url):
            if isinstance(data, list):
                new_statuses.append(handle_request(addr, data[idx]))
            else:
                new_statuses.append(handle_request(addr, data))
