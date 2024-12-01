import unittest

from messages.requests.redirect import RedirectRequest


class RedirectRequestTest(unittest.TestCase):
    def test_initialization_with_minimal_data(self):
        """
        Test initialization of RedirectRequest with required fields only.
        """
        data = {"returnUrl": "https://example.com/return", "ipAddress": "192.168.1.1", "userAgent": "Test User Agent"}
        redirect_request = RedirectRequest(**data)

        self.assertEqual(redirect_request.return_url, "https://example.com/return")
        self.assertEqual(redirect_request.ip_address, "192.168.1.1")
        self.assertEqual(redirect_request.user_agent, "Test User Agent")
        self.assertEqual(redirect_request.locale, "es_CO")
        self.assertFalse(redirect_request.capture_address)
        self.assertFalse(redirect_request.skip_result)
        self.assertFalse(redirect_request.no_buyer_fill)

    def test_initialization_with_all_fields(self):
        """
        Test initialization of RedirectRequest with all fields.
        """
        data = {
            "locale": "en_US",
            "payer": {"document": "123456789", "name": "John", "surname": "Doe"},
            "buyer": {"document": "987654321", "name": "Jane", "surname": "Doe"},
            "payment": {"reference": "TEST_REF"},
            "subscription": {"reference": "SUB123", "description": "Test Subscription"},
            "returnUrl": "https://example.com/return",
            "paymentMethod": "credit_card",
            "cancelUrl": "https://example.com/cancel",
            "ipAddress": "192.168.1.1",
            "userAgent": "Test User Agent",
            "expiration": "2023-12-31T23:59:59Z",
            "captureAddress": True,
            "skipResult": True,
            "noBuyerFill": True,
        }
        redirect_request = RedirectRequest(**data)

        self.assertEqual(redirect_request.locale, "en_US")
        self.assertEqual(redirect_request.return_url, "https://example.com/return")
        self.assertEqual(redirect_request.payment_method, "credit_card")
        self.assertEqual(redirect_request.cancel_url, "https://example.com/cancel")
        self.assertEqual(redirect_request.ip_address, "192.168.1.1")
        self.assertEqual(redirect_request.user_agent, "Test User Agent")
        self.assertEqual(redirect_request.expiration, "2023-12-31T23:59:59Z")
        self.assertTrue(redirect_request.capture_address)
        self.assertTrue(redirect_request.skip_result)
        self.assertTrue(redirect_request.no_buyer_fill)

    def test_from_dict(self):
        """
        Test creating RedirectRequest from a dictionary.
        """
        data = {"returnUrl": "https://example.com/return", "ipAddress": "192.168.1.1", "userAgent": "Test User Agent"}
        redirect_request = RedirectRequest.from_dict(data)

        self.assertIsInstance(redirect_request, RedirectRequest)
        self.assertEqual(redirect_request.return_url, "https://example.com/return")
        self.assertEqual(redirect_request.ip_address, "192.168.1.1")
        self.assertEqual(redirect_request.user_agent, "Test User Agent")

    def test_to_dict(self):
        """
        Test converting RedirectRequest to a dictionary.
        """
        data = {
            "returnUrl": "https://example.com/return",
            "ipAddress": "192.168.1.1",
            "userAgent": "Test User Agent",
            "captureAddress": True,
        }
        redirect_request = RedirectRequest(**data)
        result = redirect_request.to_dict()

        expected = {
            "locale": "es_CO",
            "payer": None,
            "buyer": None,
            "payment": None,
            "subscription": None,
            "returnUrl": "https://example.com/return",
            "paymentMethod": "",
            "cancelUrl": "",
            "ipAddress": "192.168.1.1",
            "userAgent": "Test User Agent",
            "expiration": None,
            "captureAddress": True,
            "skipResult": False,
            "noBuyerFill": False,
        }
        self.assertEqual(result, expected)

    def test_optional_fields_defaults(self):
        """
        Test that optional fields have correct default values.
        """
        data = {"returnUrl": "https://example.com/return", "ipAddress": "192.168.1.1", "userAgent": "Test User Agent"}
        redirect_request = RedirectRequest(**data)

        self.assertIsNone(redirect_request.payer)
        self.assertIsNone(redirect_request.buyer)
        self.assertIsNone(redirect_request.payment)
        self.assertIsNone(redirect_request.subscription)
        self.assertIsNone(redirect_request.expiration)
        self.assertEqual(redirect_request.payment_method, "")
        self.assertEqual(redirect_request.cancel_url, "")
