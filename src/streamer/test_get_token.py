import unittest
from utils import read_env
from dotenv import load_dotenv
from get_token import get_token
import os
class TestToken(unittest.TestCase):
    """
    """

    def test_token_retrieval(self):
        # load the environment variables from the file
        load_dotenv()
        try:
            CHROMEDRIVER = read_env("CHROMEDRIVER")
            USERNAME = read_env("USERNAME")
            PASSWORD = read_env("PASSWORD")
            PIN = read_env("PIN")
            API_KEY = read_env("API_KEY")
        except LookupError:
            print("Crucial Requirements are missing. Please review the failed variable")
            exit(1)

        # once the requirements are loaded in, lets look at the output
        request_token = get_token((USERNAME, PASSWORD, PIN), API_KEY, CHROMEDRIVER)
        self.assertEqual(type(request_token), type(" "))


if __name__ == "__main__":
    a = TestToken()
    a.test_token_retrieval()
