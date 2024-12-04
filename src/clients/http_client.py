import logging
from typing import Any, Dict, Optional

import requests

from exceptions.p2p_exception import P2PException
from exceptions.p2p_service_exception import P2pServiceException


class HttpClient:
    def __init__(self, base_url: str, timeout: int = 10, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize the HTTP client.

        :param base_url: Base URL for the API.
        :param timeout: Timeout for requests in seconds.
        :param logger: Logger instance for logging requests and responses.
        """
        self.base_url = self._sanitize_base_url(base_url)
        self.timeout = timeout
        self.logger = logger or self._default_logger()
        self.session = requests.Session()  # Use a session for better performance.

    @staticmethod
    def _sanitize_base_url(base_url: str) -> str:
        """Ensure the base URL does not end with a trailing slash."""
        return base_url.rstrip("/")

    def post(self, endpoint: str, json: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make an HTTP POST request to the specified endpoint.

        :param endpoint: The API endpoint.
        :param json: The data to include in the request body.
        :param headers: Optional HTTP headers.
        :return: Parsed JSON response as a dictionary.
        :raises P2PException: For handled HTTP errors.
        :raises P2pServiceException: For unexpected errors.
        """
        url = self._construct_url(endpoint)
        try:
            self._log_request(url, json)

            response = self.session.post(url, json=json, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            self._log_response(response)
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_request_exception(e)
        except Exception as e:
            return self._handle_generic_exception(e)

    def _construct_url(self, endpoint: str) -> str:
        """Construct the full URL for the API endpoint."""
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _log_request(self, url: str, payload: Dict[str, Any]) -> None:
        """Log the details of an outgoing request."""
        self.logger.debug("REQUEST", {"url": url, "json": payload})

    def _log_response(self, response: requests.Response) -> None:
        """Log the details of a received response."""
        self.logger.debug("RESPONSE", {"status_code": response.status_code, "result": response.text})

    def _handle_request_exception(self, exception: requests.exceptions.RequestException) -> None:
        """Handle HTTP-related exceptions."""
        if exception.response:
            self._log_warning(
                "BAD_RESPONSE",
                {
                    "class": type(exception).__name__,
                    "status_code": exception.response.status_code,
                    "result": exception.response.text,
                },
            )
        else:
            self._log_warning("BAD_RESPONSE", {"class": type(exception).__name__})

        raise P2PException.for_data_not_provided(f"Request failed: {exception}")

    def _handle_generic_exception(self, exception: Exception) -> None:
        """Handle unexpected exceptions."""
        self._log_warning(
            "EXCEPTION_RESPONSE",
            {"exception": P2PException.read_exception(exception)},
        )
        raise P2pServiceException.from_service_exception(exception)

    def _log_warning(self, label: str, context: Dict[str, Any]) -> None:
        """Log a warning message."""
        self.logger.warning(label, context)

    @staticmethod
    def _default_logger() -> logging.Logger:
        """
        Create and configure a default logger.
        """
        logger = logging.getLogger("HttpClient")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
