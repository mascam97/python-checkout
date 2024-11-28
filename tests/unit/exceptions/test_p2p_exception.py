import unittest

from exceptions.p2p_exception import P2PException


class P2PExeceptionTest(unittest.TestCase):
    def test_read_exception_with_traceback(self):
        """
        Test the read_exception method with an exception that has a traceback.
        """
        try:
            # Simulate an exception
            1 / 0
        except ZeroDivisionError as e:
            message = P2PException.read_exception(e)
            self.assertIn("ZeroDivisionError", message)
            self.assertIn("LINE", message)
            self.assertIn("ON", message)
            self.assertIn("[ZeroDivisionError]", message)

    def test_read_exception_without_traceback(self):
        """
        Test the read_exception method with an exception that has no traceback.
        """
        exception = Exception("No traceback")
        message = P2PException.read_exception(exception)
        self.assertIn("No traceback", message)
        self.assertIn("[No traceback available]", message)

    def test_for_data_not_provided(self):
        """
        Test the for_data_not_provided static method.
        """
        message = "Data not provided"
        exc = P2PException.for_data_not_provided(message)
        self.assertIsInstance(exc, P2PException)
        self.assertEqual(str(exc), message)

    def test_for_data_not_provided_empty_message(self):
        """
        Test the for_data_not_provided static method with an empty message.
        """
        exc = P2PException.for_data_not_provided()
        self.assertIsInstance(exc, P2PException)
        self.assertEqual(str(exc), "")

    def test_p2p_exception_inheritance(self):
        """
        Test that P2PException properly inherits from Exception.
        """
        exc = P2PException("Test inheritance")
        self.assertIsInstance(exc, Exception)
        self.assertEqual(str(exc), "Test inheritance")
