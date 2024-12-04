import unittest
from unittest.mock import patch

from cases.redirect_response_mock import RedirectResponseMock
from enums.status_enum import StatusEnum
from exceptions.p2p_exception import P2PException
from messages.requests.redirect import RedirectRequest
from messages.responses.information import InformationResponse
from messages.responses.redirect import RedirectResponse
from p2p_checkout import P2PCheckout


class P2PCheckoutTest(unittest.TestCase):

    def setUp(self):
        """Set up shared test data."""
        self.settings_data = {
            "base_url": "https://example.com",
            "login": "test_login",
            "tranKey": "test_tranKey",
            "timeout": 10,
        }
        self.p2p_checkout = P2PCheckout(self.settings_data)

    def test_initialization(self):
        """Test if the P2PCheckout initializes correctly."""
        self.assertIsNotNone(self.p2p_checkout.settings)
        self.assertEqual(str(self.p2p_checkout.settings.base_url), "https://example.com/")

    def test_validate_request_invalid(self):
        """Test _validate_request with an invalid type."""
        with self.assertRaises(P2PException) as context:
            self.p2p_checkout._validate_request([], RedirectRequest)

        self.assertIn("Invalid request type: list. Expected RedirectRequest.", str(context.exception))

    def test_validate_request_invalid_dict_conversion(self):
        """
        Test _validate_request with a dictionary that cannot be converted to the expected class.
        """
        invalid_dict = {"invalid_field": "value"}
        with self.assertRaises(P2PException) as context:
            self.p2p_checkout._validate_request(invalid_dict, RedirectRequest)

        self.assertIn("Failed to convert dictionary to RedirectRequest", str(context.exception))

    @patch("clients.rest_client.RestCarrier._post")
    @RedirectResponseMock.mock_response_decorator("redirect_response_successful", 200)
    def test_validate_request_valid(self, mock_post, mock_response):
        """Test _validate_request with a valid RedirectRequest and mock RestCarrier."""
        mock_post.return_value = mock_response["body"]
        redirect_request = {
            "returnUrl": "https://example.com/return",
            "ipAddress": "127.0.0.1",
            "userAgent": "P2PCheckout Sandbox",
        }

        request = self.p2p_checkout._validate_request(redirect_request, RedirectRequest)
        redirect_request = self.p2p_checkout.request(redirect_request=request)

        self.assertIsInstance(redirect_request, RedirectResponse)
        self.assertEqual(redirect_request.request_id, 1)
        self.assertEqual(
            redirect_request.process_url,
            "https://checkout-co.placetopay.dev/spa/session/1/8618851565b57b1c44d7576c4bba9b91",
        )
        self.assertEqual(redirect_request.status.status, StatusEnum.OK)
        self.assertEqual(redirect_request.status.reason, "PC")
        self.assertEqual(redirect_request.status.message, "The request has been processed correctly")
        self.assertIsNotNone(redirect_request.status.date)

    @patch("clients.rest_client.RestCarrier._post")
    @RedirectResponseMock.mock_response_decorator("information_subscription_response_successful", 200)
    def test_query_valid(self, mock_post, mock_response):
        """
        Test the query method with a valid request ID and mock response.
        """
        mock_post.return_value = mock_response["body"]

        information_response = self.p2p_checkout.query("88860")

        self.assertIsInstance(information_response, InformationResponse)
        self.assertEqual(information_response.request_id, 88860)
        self.assertEqual(information_response.status.status, "APPROVED")
        self.assertEqual(information_response.status.reason, "00")
        self.assertEqual(information_response.status.message, "The request has been successfully approved")
        self.assertIsNotNone(information_response.status.date)

        self.assertIsNotNone(information_response.request)
        self.assertEqual(information_response.request.locale, "en_US")
        self.assertEqual(information_response.request.payer.document, "118877455")
        self.assertEqual(information_response.request.payer.name, "John")
        self.assertEqual(information_response.request.return_url, "https://www.google.com")

        self.assertIsNotNone(information_response.subscription)
        self.assertEqual(information_response.subscription.type, "token")
        self.assertEqual(information_response.subscription.status.status, "OK")
        self.assertEqual(information_response.subscription.status.reason, "00")
        self.assertEqual(
            information_response.subscription.status.message, "The request has been successfully processed"
        )

        self.assertIsNotNone(information_response.subscription.instrument)
        self.assertEqual(len(information_response.subscription.instrument), 8)
        self.assertEqual(information_response.subscription.instrument[0].keyword, "token")
        self.assertEqual(
            information_response.subscription.instrument[0].value,
            "71f293122c1ed577974f2249c9449c648d8dcb104cb531f2c77e3b6c8910aca0",
        )
        self.assertEqual(information_response.subscription.instrument[1].keyword, "subtoken")
        self.assertEqual(information_response.subscription.instrument[1].value, "2964322564071111")

        self.assertIsNone(information_response.payment)

        self.assertIsNone(information_response.last_transaction())
        self.assertIsNone(information_response.last_approved_transaction())
        self.assertEqual(information_response.last_authorization(), "")
