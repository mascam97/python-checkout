import logging
from typing import Any, Dict, Optional, cast

from pydantic import BaseModel, Field, HttpUrl, model_validator
import requests

from clients.authentication import Authentication
from clients.http_client import HttpClient
from contracts.carrier import Carrier
from exceptions.p2p_exception import P2PException


class Settings(BaseModel):
    """
    Configuration class for PlaceToPay integration using Pydantic.
    """

    base_url: HttpUrl = Field(..., description="Base URL for the API")
    timeout: int = Field(default=15, description="Request timeout in seconds")
    login: str = Field(..., description="API login key")
    tranKey: str = Field(..., description="API transaction key")
    additional_headers: Dict[str, str] = Field(default_factory=dict, description="Additional HTTP headers")
    authAdditional: Dict[str, Any] = Field(
        default_factory=dict,
        alias="authAdditional",
        description="Additional authentication data",
    )
    loggerConfig: Optional[Dict[str, Any]] = Field(default=None, description="Logger configuration")

    _logger: Optional[logging.Logger] = None
    _carrier_instance: Optional[Carrier] = None
    _client: Optional[requests.Session] = None

    @model_validator(mode="before")
    @classmethod
    def validate_base_url(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure the base_url ends with a slash and is valid.
        """
        base_url = values.get("base_url")
        if not base_url:
            raise ValueError("Base URL cannot be empty.")

        values["base_url"] = f"{str(base_url).rstrip('/')}/"
        return values

    def base_url_with_endpoint(self, endpoint: str = "") -> str:
        """
        Construct the full URL for a given endpoint.

        :param endpoint: API endpoint.
        :return: Full URL as a string.
        """
        return f"{str(self.base_url).rstrip('/')}/{endpoint.lstrip('/')}"

    def get_client(self) -> HttpClient:
        """
        Return or create the HTTP client instance.

        :return: Configured `HttpClient`.
        :raises P2PException: If the existing client is not an instance of HttpClient.
        """
        if not self._client:
            self._client = HttpClient(
                base_url=str(self.base_url),
                timeout=self.timeout,
                logger=self.logger(),
            )
        elif not isinstance(self._client, HttpClient):
            raise P2PException.for_data_not_provided(
                f"Invalid client type: Expected HttpClient, got {type(self._client).__name__}"
            )
        client = cast(HttpClient, self._client)
        client.session.headers.update(self.additional_headers)
        return client

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
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        if self.loggerConfig:
            logger.setLevel(self.loggerConfig.get("level", logging.DEBUG))
            custom_formatter = self.loggerConfig.get("formatter")
            if custom_formatter:
                logger.handlers[0].setFormatter(logging.Formatter(custom_formatter))

        return logger

    def authentication(self) -> Authentication:
        """
        Return an `Authentication` instance.
        """
        auth = Authentication(
            {
                "login": self.login,
                "tranKey": self.tranKey,
                "authAdditional": self.authAdditional,
            }
        )
        return auth

    def carrier(self) -> Carrier:
        """
        Return or create the carrier instance.
        """
        from clients.rest_client import RestCarrier

        if not self._carrier_instance:
            self._carrier_instance = RestCarrier(self)
        return self._carrier_instance
