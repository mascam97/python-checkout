import unittest
from unittest import mock
from clients.authentication import Authentication
from contracts.carrier import Carrier
from clients.rest_client import RestCarrier
from entities.settings import Settings


class SettingsTest(unittest.TestCase):

    def setUp(self):
        self.config = {
            "baseUrl": "https://example.com/",
            "timeout": 10,
            "login": "test_login",
            "tranKey": "test_tranKey",
            "authAdditional": {},
            "loggerConfig": {"level": "DEBUG"},
            "additional_headers": {"Authorization": "Bearer test_token"},
        }

    def test_base_url_with_endpoint(self):
        settings = Settings(**self.config)
        url = settings.base_url_with_endpoint("test-endpoint")
        self.assertEqual(url, "https://example.com/test-endpoint")

    def test_get_client(self):
        settings = Settings(**self.config)
        client = settings.get_client()
        self.assertIsNotNone(client)
        print(client.headers)
        self.assertEqual(client.headers, {'User-Agent': 'python-requests/2.32.3', 'Accept-Encoding': 'gzip, deflate',
                         'Accept': '*/*', 'Connection': 'keep-alive', 'Authorization': 'Bearer test_token'})
        self.assertEqual(client.timeout, self.config["timeout"])

    @mock.patch("entities.settings.Authentication")
    def test_authentication_instance(self, MockAuth):
        settings = Settings(**self.config)
        auth = settings.authentication()

        MockAuth.assert_called_once_with({
            "login": self.config["login"],
            "tranKey": self.config["tranKey"],
            "authAdditional": self.config["authAdditional"]
        })

    def test_rest_client_instance(self):
        settings = Settings(**self.config)
        self.assertIsInstance(settings.carrier(), RestCarrier)
