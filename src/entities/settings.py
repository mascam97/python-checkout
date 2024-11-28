import requests
import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, model_validator, ConfigDict
from clients.authentication import Authentication
from contracts.carrier import Carrier


class Settings(BaseModel):
    """
    Configuration class for PlaceToPay integration using Pydantic.
    """

    base_url: HttpUrl = Field(..., description="Base URL for the API")
    timeout: int = Field(default=15, description="Request timeout in seconds")
    login: str = Field(..., description="API login key")
    tranKey: str = Field(..., description="API transaction key")
    additional_headers: Dict[str, str] = Field(
        default_factory=dict, description="Additional HTTP headers"
    )
    authAdditional: Dict[str, Any] = Field(
        default_factory=dict,
        alias="authAdditional",
        description="Additional authentication data",
    )
    loggerConfig: Optional[Dict[str, Any]] = Field(
        default=None, description="Logger configuration")

    _logger: Optional[logging.Logger] = None
    _carrier_instance: Optional[Carrier] = None
    _client: Optional[requests.Session] = None

    @model_validator(mode="before")
    @classmethod
    def validate_base_url(cls, values: dict) -> dict:
        """
        Ensure the base_url ends with a slash and is valid.
        """
        if not values["base_url"]:
            raise ValueError("Base URL cannot be empty.")

        values["base_url"] = f'{values["base_url"].rstrip("/")}/' if "base_url" in values else values["base_url"]
        return values

    def base_url_with_endpoint(self, endpoint: str = "") -> str:
        """
        Construct the full URL for a given endpoint.

        :param endpoint: API endpoint.
        :return: Full URL as a string.
        """
        return str(self.base_url) + endpoint

    def get_client(self) -> requests.Session:
        """
        Return or create the HTTP client instance.

        :return: Configured `requests.Session`.
        """
        if not self._client:
            self._client = requests.Session()

            self._client.headers.update(self.additional_headers)
            self._client.timeout = self.timeout
        return self._client

    def logger(self) -> logging.Logger:
        """
        Configure and return the logger.
        """
        if not self._logger:
            self._logger = self._create_logger()
        return self._logger

    def _create_logger(self) -> logging.Logger:
        """
        Create and configure a logger based on logger_config or a default setup.

        :return: Configured logger instance.
        """
        logger = logging.getLogger("P2P Checkout Logger")
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        else:
            handler = logger.handlers[0]

        if self.loggerConfig:
            logger.setLevel(self.loggerConfig.get("level", logging.DEBUG))
            custom_formatter = self.loggerConfig.get("formatter")
            if custom_formatter:
                handler.setFormatter(logging.Formatter(custom_formatter))

        return logger

    def authentication(self) -> Authentication:
        """
        Return an `Authentication` instance.
        """
        auth = Authentication({
            "login": self.login,
            "tranKey": self.tranKey,
            "authAdditional": self.authAdditional,
        })
        return auth

    def carrier(self) -> Carrier:
        """
        Return or create the carrier instance.
        """
        from clients.rest_client import RestCarrier  # Deferred import
        return RestCarrier(self)
