import unittest
import logging
from unittest import mock
from unittest.mock import MagicMock
from clients.rest_client import RestCarrier
from entities.settings import Settings
from clients.http_client import HttpClient


class SettingsTest(unittest.TestCase):

    def setUp(self):
        self.config = {
            "base_url": "https://example.com/",
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
        self.assertEqual(client.session.headers, {'User-Agent': 'python-requests/2.32.3', 'Accept-Encoding': 'gzip, deflate',
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

    def test_validate_base_url_with_missing_slash(self):
        config = self.config.copy()
        config["base_url"] = "https://example.com"
        settings = Settings(**config)
        self.assertEqual(str(settings.base_url), "https://example.com/")

    def test_validate_base_url_with_empty_url(self):
        config = self.config.copy()
        config["base_url"] = ""
        with self.assertRaises(ValueError) as context:
            Settings(**config)
        self.assertIn("Base URL cannot be empty.", str(context.exception))

    def test_logger_creation(self):
        config = self.config.copy()
        settings = Settings(**config)
        logger = settings.logger()
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)

    def test_create_logger_with_custom_formatter(self):
        config = self.config.copy()
        config["loggerConfig"]["formatter"] = "%(message)s"
        settings = Settings(**config)
        logger = settings.logger()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertEqual(len(logger.handlers), 1)

    def test_client_headers_and_timeout(self):
        settings = Settings(**self.config)
        client = settings.get_client()

        self.assertEqual(client.session.headers["Authorization"], "Bearer test_token")
        self.assertEqual(client.timeout, self.config["timeout"])

    def test_get_client_initializes_session(self):
        """
        Test that get_client initializes a HttpClient with headers and timeout.
        """
        settings = Settings(**self.config)
        client = settings.get_client()

        self.assertIsInstance(client, HttpClient)
        self.assertEqual(client.session.headers["Authorization"], "Bearer test_token")
        self.assertEqual(client.timeout, self.config["timeout"])

    def test_get_client_uses_existing_session(self):
        """
        Test that get_client reuses an existing session if already initialized.
        """
        settings = Settings(**self.config)
        first_client = settings.get_client()
        second_client = settings.get_client()
        self.assertIs(first_client, second_client)

        # Verifica que el cliente sigue siendo una instancia de HttpClient
        self.assertIsInstance(first_client, HttpClient)

    def test_logger_reuses_existing_instance(self):
        """
        Test that logger() reuses the existing _logger instance if already initialized.
        """
        settings = Settings(**self.config)

        existing_logger = MagicMock()
        settings._logger = existing_logger

        logger = settings.logger()
        self.assertEqual(logger, existing_logger)

    def test_custom_logger_configuration(self):
        """
        Test that custom logger configuration is applied correctly.
        """
        custom_config = {
            "level": logging.ERROR,
            "formatter": "%(message)s",
        }
        self.config["loggerConfig"] = custom_config
        settings = Settings(**self.config)
        logger = settings._create_logger()

        self.assertEqual(logger.level, logging.ERROR)
