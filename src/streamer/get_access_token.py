"""
Module to make an access token from a request token from zerodha's kite api
"""
import requests
from utils import get_sha_256 as sha256
import json
def get_access_token(api_bundle, request_token):
    """For a given api bundle and request token, returns the access token after making a call to kite's login api

    Args:
        api_bundle (tuple): Bundle of the API_KEY and the API_SECRET
        request_token (str): The request token obtained from the kite login flow

    Returns:
        json: A JSON with the API key and request token, everything needed to start the kite websocket stream
    """
    try:
        # try and unpack the API key and the API secret from the bundle
        api_key, api_secret = api_bundle
    except ValueError:
        # raise a value error if this fails
        raise ValueError("API Bundle did not contain key and secret in the right order") from None
    
    # generate a checksum from the three pieces of essential data
    checksum = str(sha256(api_key + request_token + api_secret))
    # construct the JSON data for the request
    data = {
            "api_key": api_key,
            "request_token": request_token,
            "checksum": checksum
            }
    # set the request URL
    url = "https://api.kite.trade/session/token"
    # set the header for the request
    header = {
            "X-Kite-Version": "3"
            }
    # send the response
    response = requests.post(url, data, headers=header)
    # return the response
    return json.loads(response.content)["data"]["access_token"]

