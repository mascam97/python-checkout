import logging
from typing import Dict, Optional

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
        self.base_url = str(base_url).rstrip("/")
        self.timeout = timeout
        self.logger = logger or self._default_logger()
        self.session = requests.Session()  # Use a session for better performance.

    def post(self, endpoint: str, json: Dict, headers: Optional[Dict[str, str]] = None) -> Dict:
        """
        Make an HTTP POST request to the specified endpoint.

        :param endpoint: The API endpoint.
        :param json: The data to include in the request body.
        :param headers: Optional HTTP headers.
        :return: Parsed JSON response as a dictionary.
        :raises P2PException: For handled HTTP errors.
        :raises P2pServiceException: For unexpected errors.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            # Log the request
            if self.logger:
                self.logger.debug("REQUEST", {"url": url, "json": json})

            # Send the POST request
            response = self.session.post(url, json=json, headers=headers, timeout=self.timeout)

            # Raise an exception for HTTP errors (e.g., 4xx or 5xx)
            response.raise_for_status()

            # Log the response
            if self.logger:
                self.logger.debug("RESPONSE", {"status_code": response.status_code, "result": response.text})

            # Parse and return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            if e.response:
                if self.logger:
                    self.logger.warning(
                        "BAD_RESPONSE",
                        {"class": type(e).__name__, "status_code": e.response.status_code, "result": e.response.text},
                    )
            else:
                if self.logger:
                    self.logger.warning("BAD_RESPONSE", {"class": type(e).__name__})

            raise P2PException.for_data_not_provided(f"Request failed: {e}")
        except Exception as e:
            if self.logger:
                self.logger.warning(
                    "EXCEPTION_RESPONSE",
                    {"exception": P2PException.read_exception(e)},
                )
            raise P2pServiceException.from_service_exception(e)

    def _default_logger(self) -> logging.Logger:
        """
        Create a default logger if none is provided.
        """
        import logging

        logger = logging.getLogger("HttpClient")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
