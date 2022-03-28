"""
Module to stream data from the KITE API via a websocket connection
"""
import logging
import sys
from kiteconnect import KiteTicker
from dotenv import load_dotenv
from get_token import get_token
from utils import read_env
from get_access_token import get_access_token
# Load the environment variables
load_dotenv()
## LOADING ENV VARS FROM .env
try:
    API_KEY = read_env("API_KEY")
    API_SECRET = read_env("API_SECRET")
    LOGIN = read_env("USERNAME")
    PASSW = read_env("PASSWORD")
    PIN = read_env("PIN")
    STREAMER_PATH = read_env("CHROMEDRIVER")
except LookupError as err:
    raise LookupError("Did not find the following env variable") from err

logging.basicConfig(level=logging.DEBUG)

REQUEST_TOKEN = get_token((LOGIN, PASSW, PIN), API_KEY, STREAMER_PATH)
ACCESS_TOKEN = get_access_token((API_KEY, API_SECRET), REQUEST_TOKEN)
# Check if we've already got an access token.
if not ACCESS_TOKEN:
    print("Access token not found.")
    sys.exit(1)
else:
    try:
        # Initialise Kite Connect object with access token.
        kws = KiteTicker(API_KEY, ACCESS_TOKEN)
        print("Init Kite Done!!!!!!")
    except ValueError:
        raise ValueError("Invalid API key or Access token") from None


def on_ticks(ws, ticks):
    """Callback to receive ticks."""
    logging.debug("Ticks: %s", ticks)

def on_connect(ws, response):
    """Callback on successful connect.
    Subscribe to a list of instrument_tokens (RELIANCE and ACC here)."""
    ws.subscribe([2714625, 128083204])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [2714625, 128083204])
def on_close(ws, code, reason):
    """On connection close stop the main loop
    Reconnection will not happen after executing `ws.stop()`"""
    ws.stop()

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
