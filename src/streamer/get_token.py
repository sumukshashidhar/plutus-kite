"""
Module to retrieve REQUEST_TOKENS from Zerodha's Kite
"""
import time
import platform
import sys
from urllib.parse import urlparse, parse_qs
from selenium import webdriver # pylint: disable=import-error
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities # pylint: disable=import-error
from pyvirtualdisplay import Display # pylint: disable=import-error



def get_token(auth, api_key, streamer_path):
    """Feteches a request token from Kite using the auth parameters, an API Key and a webdriver path

    Args:
        auth (tuple): Tuple where index 0 - username, 1 - password, 2 - pin.
        api_key (str): The Kite Trade API key
        streamer_path (str): Path to the selenium webdriver installation

    Raises:
        ValueError: In case the auth tuple is not wrong

    Returns:
        str: The request token.
    """
    try:
        # unpack the arguments from the auth combination
        username, password, pin = auth
    except ValueError:
        raise ValueError("Auth object did not contain exactly username, \
            password and pin in the required order") from None

    # make a virtual display so that docker understands
    # do this only if we are not on macos / windows
    if platform.system() != "Darwin":
        display = Display(visible=0, size=(800, 600))
        display.start()

    # define some desired capabilities
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"

    # set default options for chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    # make the chrome driver using options and webdriver location
    driver = webdriver.Chrome(
        executable_path=streamer_path,
        options=options,
        desired_capabilities=caps,
    )

    # get the URL link:
    driver.get(f"https://kite.zerodha.com/connect/login?v=3&api_key={api_key}")

    # sleep until the URL is retrieved
    time.sleep(1)

    # send the username and password as keys
    driver.find_element_by_xpath('//*[@id="userid"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)

    # click the submit button
    driver.find_element_by_xpath(
        '//*[@id="container"]/div/div/div/form/div[4]/button'
    ).click()

    # wait for some more time until the page loads, and then send the pin
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="pin"]').send_keys(pin)
    driver.find_element_by_xpath(
        '//*[@id="container"]/div/div/div[2]/form/div[3]/button'
    ).click()

    # wait for the request processes, and then grab the current url
    time.sleep(0.5)
    url = driver.current_url

    return parse_qs(urlparse(url).query)["request_token"][0]

if __name__ == "__main__":
    print("This module is not meant to be run independently. \
        Please run it through either hte main file or the streamer files, or as a test case.")
    sys.exit(0)
