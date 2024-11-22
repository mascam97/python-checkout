import unittest
from src.entities.settings import Settings


class SettingsTest(unittest.TestCase):

    def test_settings_initialization(self):
        config = {
            "baseUrl": "https://example.com",
            "login": "test_login",
            "tranKey": "test_key",
            "timeout": 10,
            "verifySsl": True,
        }
        settings = Settings(**config)
        assert str(settings.baseUrl) == "https://example.com/"
        assert settings.login == "test_login"
        assert settings.tranKey == "test_key"
