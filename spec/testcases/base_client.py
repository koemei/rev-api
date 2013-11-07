import unittest

from rev.base_client import BaseClient


class BaseClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = BaseClient()

    def tearDown(self):
        self.client = None

    def test_config(self):
        if not hasattr(self.client, "_user_api_key") or self.client._user_api_key is None:
            self.fail("user api key not set")
        if not hasattr(self.client, "_client_api_key") or self.client._client_api_key is None:
            self.fail("client api key not set")
        if not hasattr(self.client, "base_path") or self.client.base_path is None:
            self.fail("base path not set")

if __name__ == "__main__":
    unittest.main()