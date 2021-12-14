"""Handles utility functions for the WLED and weather classes."""
# https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module


def handle_request(request):
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
    try:
        return request.json()
    except:
        return "Invalid request"
