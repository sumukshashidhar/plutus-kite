"""
Module to stream data from the KITE API via a websocket connection
"""
import logging
import sys
from kiteconnect import KiteTicker
from dotenv import load_dotenv
from get_token import get_token
from utils import read_env
# Load the environment variables
load_dotenv()
## LOADING ENV VARS FROM .env
try:
    API_KEY = read_env("API_KEY")
    API_SECRET = read_env("API_SECRET")
    LOGIN = read_env("LOGIN")
    PASSW = read_env("PASSW")
    PIN = read_env("PIN")
    STREAMER_PATH = read_env("STREAMER_PATH")
except LookupError as err:
    raise LookupError("Did not find the following env variable") from err

logging.basicConfig(level=logging.DEBUG)

ACCESS_TOKEN = get_token((LOGIN, PASSW, PIN), API_KEY, STREAMER_PATH)

# Check if we've already got an access token.
if not ACCESS_TOKEN:
    print("Access token not found.")
    sys.exit(1)
else:
    try:
        # Initialise Kite Connect object with access token.
        kws = KiteTicker(API_KEY, ACCESS_TOKEN)
    except ValueError:
        raise ValueError("Invalid API key or Access token") from None


def on_ticks(web_socket, ticks):
    """Callback to receive ticks."""
    logging.debug("Ticks: %s", ticks)

def on_connect(web_socket, response):
    """Callback on successful connect.
    Subscribe to a list of instrument_tokens (RELIANCE and ACC here)."""
    web_socket.subscribe([738561, 5633])

    # Set RELIANCE to tick in `full` mode.
    web_socket.set_mode(web_socket.MODE_FULL, [738561])
def on_close(web_socket, code, reason):
    """On connection close stop the main loop
    Reconnection will not happen after executing `ws.stop()`"""
    web_socket.stop()

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
