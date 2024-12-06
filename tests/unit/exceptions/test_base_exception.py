import unittest

from exceptions.base_exception import BaseException


class BaseExceptionTest(unittest.TestCase):

    def test_initialization_with_all_params(self):
        """
        Test initialization with all parameters.
        """
        exc = BaseException(
            message="Test error",
            status_code=400,
            details={"code": "BAD_REQUEST", "info": "Invalid input"},
        )
        self.assertEqual(exc.message, "Test error")
        self.assertEqual(exc.status_code, 400)
        self.assertEqual(exc.details, {"code": "BAD_REQUEST", "info": "Invalid input"})

    def test_initialization_with_defaults(self):
        """
        Test initialization with default parameters.
        """
        exc = BaseException(message="Default error")
        self.assertEqual(exc.message, "Default error")
        self.assertIsNone(exc.status_code)
        self.assertEqual(exc.details, {})

    def test_to_dict_with_all_params(self):
        """
        Test the to_dict method with all parameters.
        """
        exc = BaseException(
            message="Test error",
            status_code=404,
            details={"resource": "User", "action": "Fetch"},
        )
        expected_dict = {
            "error": "Test error",
            "status_code": 404,
            "details": {"resource": "User", "action": "Fetch"},
        }
        self.assertEqual(exc.to_dict(), expected_dict)

    def test_to_dict_with_defaults(self):
        """
        Test the to_dict method with default parameters.
        """
        exc = BaseException(message="Error with defaults")
        expected_dict = {
            "error": "Error with defaults",
            "status_code": None,
            "details": {},
        }
        self.assertEqual(exc.to_dict(), expected_dict)

    def test_str_with_all_params(self):
        """
        Test the __str__ method with all parameters.
        """
        exc = BaseException(
            message="Test error",
            status_code=500,
            details={"code": "SERVER_ERROR", "trace": "stack_trace"},
        )
        expected_str = "Test error (Status Code: 500) | Details: {'code': 'SERVER_ERROR', 'trace': 'stack_trace'}"
        self.assertEqual(str(exc), expected_str)

    def test_str_with_message_only(self):
        """
        Test the __str__ method with message only.
        """
        exc = BaseException(message="Simple error")
        self.assertEqual(str(exc), "Simple error")

    def test_str_with_message_and_status_code(self):
        """
        Test the __str__ method with message and status code.
        """
        exc = BaseException(message="Error with code", status_code=403)
        expected_str = "Error with code (Status Code: 403)"
        self.assertEqual(str(exc), expected_str)

    def test_str_with_message_and_details(self):
        """
        Test the __str__ method with message and details.
        """
        exc = BaseException(message="Error with details", details={"key": "value"})
        expected_str = "Error with details | Details: {'key': 'value'}"
        self.assertEqual(str(exc), expected_str)
