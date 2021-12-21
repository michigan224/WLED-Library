"""Handles utility functions for the WLED and weather classes."""
import logging

import requests

logger = logging.getLogger(__name__)


def handle_request(url, body=None):
    """
    Handle the request.

    Parameters
    ----------
    request : str
        The request from the client.

    Returns
    -------
    str
        The response to the client.
    """
    logger.info("Handling request: %s", url)
    try:
        if not body:
            request = requests.get(url)
        else:
            request = requests.post(url, json=body)
        request.raise_for_status()
        return request.json()
    except requests.exceptions.HTTPError as errh:
        logging.error('HTTP error: %s', errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        logging.error('Error Connecting: %s', errc)
        return None
    except requests.exceptions.Timeout as errt:
        logging.error('Timeout Error: %s', errt)
        return None
    except requests.exceptions.RequestException as err:
        logging.error('Error: %s', err)
        return None


def weather_to_data(weather: dict) -> dict:
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
