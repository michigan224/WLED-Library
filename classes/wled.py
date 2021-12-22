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

    def __str__(self) -> str:
        """
        Return string representation of Wled.

        Returns
        -------
        String representation of Wled.
        """
        return f"WLED(s): {', '.join(self.wled_ip)}"

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
        for url_addr in self.url:
            statuses.append(handle_request(url_addr))
        return statuses

    def __create_update_data(self, data: Union[dict, list]) -> Union[dict, list]:
        """
        Create data to be passed to the lights.

        Parameters
        ----------
        data : dictionary
            Updated state to be passed to the lights.

        Returns
        -------
        Data to be passed to the lights.
        """
        curr_state = self.get_status()
        data = [data] if isinstance(data, dict) else data
        if len(data) > len(self.url):
            raise DataNotInRangeError(data, self.url)
        for idx, upd in enumerate(data):
            if 'seg' in upd:
                for seg_idx, seg in enumerate(upd['seg']):
                    palette = curr_state[idx]['seg'][seg_idx]['pal']
                    effect = curr_state[idx]['seg'][seg_idx]['fx']
                    effect_speed = curr_state[idx]['seg'][seg_idx]['sx']
                    effect_intensity = curr_state[idx]['seg'][seg_idx]['ix']
                    if 'pal' in seg and seg['pal'] == palette:
                        del seg['pal']
                    if 'fx' in seg and seg['fx'] == effect:
                        del seg['fx']
                    if 'sx' in seg and seg['sx'] == effect_speed:
                        del seg['sx']
                    if 'ix' in seg and seg['ix'] == effect_intensity:
                        del seg['ix']
        return data

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
            return [handle_request(f"http://{ip_addr}/json/state", self.__create_update_data(data))]
        new_statuses = []
        parsed_data = self.__create_update_data(data)
        for idx, upd_data in enumerate(parsed_data):
            new_statuses.append(handle_request(self.url[idx], upd_data))
        return new_statuses


class DataNotInRangeError(Exception):
    """
    Exception for when data is not in range.

    Parameters
    ----------
    data : str
        Data that is not in range.
    """

    def __init__(self, data: list, ip_list: list) -> None:
        """
        Initialize DataNotInRangeError class.

        Parameters
        ----------
        data : str
            Data that is not in range.
        """
        self.data_length = len(data)
        self.ip_list_length = len(ip_list)

    def __str__(self) -> str:
        """
        Return string representation of DataNotInRangeError.

        Returns
        -------
        String representation of DataNotInRangeError.
        """
        return f"Tried to update {self.data_length} lights, but only {self.ip_list_length} connected."
