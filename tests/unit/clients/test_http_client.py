import unittest
from unittest.mock import MagicMock, patch

import requests
from requests.models import Response

from clients.http_client import HttpClient
from exceptions.p2p_exception import P2PException
from exceptions.p2p_service_exception import P2pServiceException


class TestHttpClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com"
        self.client = HttpClient(self.base_url)

    def _mock_response(self, status_code=200, json_data=None, raise_for_status=None):
        """Helper to mock a requests response."""
        mock_resp = unittest.mock.Mock(spec=Response)
        mock_resp.status_code = status_code
        mock_resp.json = unittest.mock.Mock(return_value=json_data or {})
        mock_resp.raise_for_status = unittest.mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        return mock_resp

    @patch("requests.Session.post")
    def test_post_successful_request(self, mock_post):
        """Test a successful POST request."""
        mock_post.return_value = self._mock_response(status_code=200, json_data={"key": "value"})

        response = self.client.post(endpoint="/test", json={"data": "test"})

        self.assertEqual(response, {"key": "value"})
        mock_post.assert_called_once_with(
            f"{self.base_url}/test",
            json={"data": "test"},
            headers=None,
            timeout=10,
        )

    @patch("requests.Session.post")
    def test_post_http_error(self, mock_post):
        """Test a POST request that raises an HTTP error."""
        mock_post.return_value = self._mock_response(
            status_code=400,
            raise_for_status=requests.exceptions.HTTPError("Bad Request"),
        )

        with self.assertRaises(P2PException) as context:
            self.client.post(endpoint="/test", json={"data": "test"})

        self.assertIn("Request failed", str(context.exception))
        mock_post.assert_called_once()

    @patch("requests.Session.post")
    def test_post_generic_exception(self, mock_post):
        """Test a POST request that raises a generic exception."""
        mock_post.side_effect = Exception("Something went wrong")

        with self.assertRaises(P2pServiceException) as context:
            self.client.post(endpoint="/test", json={"data": "test"})

        self.assertIn("Something went wrong", str(context.exception))
        mock_post.assert_called_once()

    def test_sanitize_base_url(self):
        """Test that the base URL is sanitized correctly."""
        client = HttpClient("https://example.com/")
        self.assertEqual(client.base_url, "https://example.com")

    def test_handle_request_exception_with_response(self):
        """
        Test handling of a RequestException that includes a response.
        """
        response_mock = MagicMock()
        response_mock.status_code = 400
        response_mock.text = "Bad Request"

        exception = requests.exceptions.RequestException()
        exception.response = response_mock

        # Replace the logger with a mock to verify logging
        self.client.logger = MagicMock()

        # Call the private method `_handle_request_exception` to test it
        with self.assertRaises(Exception):  # Adjust exception type if needed
            self.client._handle_request_exception(exception)

        # Verify that the logger warning was called with the correct parameters
        self.client.logger.warning.assert_called_once_with(
            "BAD_RESPONSE",
            {
                "class": "RequestException",
                "status_code": 400,
                "result": "Bad Request",
            },
        )
