import logging
import unittest
from unittest.mock import MagicMock

from clients.http_client import HttpClient
from clients.rest_client import RestCarrier
from entities.settings import Settings


class SettingsTest(unittest.TestCase):

    def setUp(self):
        self.config = {
            "base_url": "https://example.com/",
            "timeout": 10,
            "login": "test_login",
            "tranKey": "test_tranKey",
            "auth_additional": {},
            "loggerConfig": {"level": "DEBUG"},
            "headers": {"Authorization": "Bearer test_token"},
        }

    def test_base_url_with_endpoint(self):
        settings = Settings(**self.config)
        url = settings.base_url_with_endpoint("test-endpoint")
        self.assertEqual(url, "https://example.com/test-endpoint")

    def test_get_client(self):
        settings = Settings(**self.config)
        client = settings.get_client()
        carrier = settings.carrier()
        self.assertIsInstance(carrier, RestCarrier)
        self.assertIsInstance(client, HttpClient)
        self.assertEqual(client.headers["Authorization"], "Bearer test_token")
        self.assertEqual(client.timeout, self.config["timeout"])

    def test_authentication_instance(self):
        settings = Settings(**self.config)
        auth = settings.authentication()
        self.assertEqual(auth.login, self.config["login"])
        self.assertEqual(auth.tran_key, self.config["tranKey"])
        self.assertEqual(auth.additional, self.config["auth_additional"])

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
        settings = Settings(**self.config)
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
        handler = logger.handlers[0]
        self.assertIsInstance(handler.formatter, logging.Formatter)
        self.assertEqual(handler.formatter._fmt, "%(message)s")

    def test_client_headers_and_timeout(self):
        settings = Settings(**self.config)
        client = settings.get_client()
        self.assertEqual(client.headers["Authorization"], "Bearer test_token")
        self.assertEqual(client.timeout, self.config["timeout"])

    def test_get_client_initializes_session(self):
        settings = Settings(**self.config)
        client = settings.get_client()
        self.assertIsInstance(client, HttpClient)
        self.assertEqual(client.headers["Authorization"], "Bearer test_token")
        self.assertEqual(client.timeout, self.config["timeout"])

    def test_get_client_uses_existing_session(self):
        settings = Settings(**self.config)
        first_client = settings.get_client()
        second_client = settings.get_client()
        self.assertIs(first_client, second_client)
        self.assertIsInstance(first_client, HttpClient)

    def test_logger_reuses_existing_instance(self):
        settings = Settings(**self.config)
        existing_logger = MagicMock()
        settings.p2p_logger = existing_logger
        logger = settings.logger()
        self.assertEqual(logger, existing_logger)

    def test_custom_logger_configuration(self):
        config = self.config.copy()
        config.pop("loggerConfig", None)
        settings = Settings(**config)
        logger = settings.logger()

        self.assertIsNotNone(logger)
        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.level, logging.DEBUG)

    def test_create_logger_with_logger_config(self):
        config = self.config.copy()
        config["loggerConfig"] = {"level": logging.WARNING, "formatter": "%(message)s"}
        settings = Settings(**config)
        logger = settings.logger()
        self.assertEqual(logger.level, logging.WARNING)
        self.assertEqual(len(logger.handlers), 1)
        handler = logger.handlers[0]
        self.assertIsInstance(handler.formatter, logging.Formatter)
        self.assertEqual(handler.formatter._fmt, "%(message)s")

    def test_use_external_client(self):
        """
        Test that get_client uses an externally provided HttpClient.
        """
        external_client = HttpClient(base_url="https://external_client.com", timeout=120, logger=None, headers=None)
        self.config["p2p_client"] = external_client
        settings = Settings(**self.config)

        client = settings.get_client()
        self.assertEqual(client, external_client)
        self.assertEqual(client.headers, {})
