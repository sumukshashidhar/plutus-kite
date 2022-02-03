"""
Unittest to test the efficacy of the selenium access token extractor.
"""
import unittest
import sys
from dotenv import load_dotenv
from utils import read_env
from get_token import get_token

class TestToken(unittest.TestCase):
    """
    Tests the efficacy of the selenium token extractor.
    """

    def test_token_retrieval(self):
        """Send env variables to the selenium token extractor and extract the refresh token
        """
        # load the environment variables from the file
        load_dotenv()
        try:
            chromedriver = read_env("CHROMEDRIVER")
            username = read_env("USERNAME")
            password = read_env("PASSWORD")
            pin = read_env("PIN")
            api_key = read_env("API_KEY")
        except LookupError:
            print("Crucial Requirements are missing. Please review the failed variable")
            sys.exit(1)

        # once the requirements are loaded in, lets look at the output
        request_token = get_token((username, password, pin), api_key, chromedriver)
        self.assertEqual(type(request_token), type(" "))
