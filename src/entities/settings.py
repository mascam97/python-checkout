import requests, logging
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, model_validator, ConfigDict
from client.authentication import Authentication
from contracts.carrier import Carrier


class Settings(BaseModel):
    """
    Configuration class for PlaceToPay integration using Pydantic.
    """

    baseUrl: HttpUrl = Field(..., description="Base URL for the API")
    timeout: int = Field(default=15, description="Request timeout in seconds")
    verifySsl: bool = Field( default=True, description="Verify SSL certificates")
    login: str = Field(..., description="API login key")
    tranKey: str = Field(..., description="API transaction key")
    headers: Dict[str, str] = Field(
        default_factory=dict, description="Additional HTTP headers"
    )
    authAdditional: Dict[str, Any] = Field(
        default_factory=dict,
        alias="authAdditional",
        description="Additional authentication data",
    )
    loggerConfig: Optional[Dict[str, Any]] = Field(default=None, description="Logger configuration")

    # Internal fields
    _logger: Optional[logging.Logger] = None
    _carrier_instance: Optional[Carrier] = None

    @model_validator(mode="before")
    @classmethod
    def validate_base_url(cls, values: dict) -> dict:
        """
        Ensure the base_url ends with a slash.

        :param values: Input values for the model.
        :return: Modified values with a corrected base_url.
        """
        if "base_url" in values and not values["base_url"].endswith("/"):
            values["base_url"] += "/"
        return values

    def base_url_with_endpoint(self, endpoint: str = "") -> str:
        """
        Construct the full URL for a given endpoint.

        :param endpoint: API endpoint.
        :return: Full URL as a string.
        """
        return self.baseUrl + endpoint

    def timeout(self) -> int:
        """
        Return the timeout for requests.
        """
        return self.timeout

    def verifySsl(self) -> bool:
        """
        Return whether SSL verification is enabled.
        """
        return self.verifySsl

    def headers(self) -> Dict[str, str]:
        """
        Return the additional headers for requests.
        """
        return self.headers

    def client(self) -> requests.Session:
        """
        Return or create the HTTP client instance.

        :return: Configured `requests.Session`.
        """
        if not self.client:
            self.client = requests.Session()
            self.client.headers.update(self.headers)
            self.client.verify = self.verifySsl
            self.client.timeout = self.timeout
        return self.client

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

        # Add handler if it doesn't exist
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Apply custom configurations if provided
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
        return Authentication(
            {
                "login": self.login,
                "tranKey": self.tranKey,
                "authAdditional": self.authAdditional,
            }
        )

    def carrier(self) -> Carrier:
        """
        Return or create the carrier instance.
        """
        if not self._carrier_instance:
            from client.rest_client import (
                RestCarrier,
            )  # Deferred import to avoid circular dependencies

            self._carrier_instance = RestCarrier(self)
        return self._carrier_instance

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the settings object to a dictionary.
        """
        return {
            "baseUrl": self.baseUrl,
            "timeout": self.timeout,
            "verifySsl": self.verifySsl,
            "login": self.login,
            "tranKey": self.tranKey,
            "headers": self.headers,
            "authAdditional": self.authAdditional,
        }
