import unittest
from exceptions.p2p_exception import P2PException
from exceptions.p2p_service_exception import P2pServiceException


class P2pServiceExceptionTest(unittest.TestCase):
    def test_from_service_exception_with_traceback(self):
        """
        Test creating P2pServiceException from an exception with a traceback.
        """
        try:
            # Simulate an exception
            1 / 0
        except ZeroDivisionError as e:
            exc = P2pServiceException.from_service_exception(e)
            self.assertIsInstance(exc, P2pServiceException)
            self.assertIn("Error handling operation", str(exc))
            self.assertIn("line", str(exc))

    def test_from_service_exception_without_traceback(self):
        """
        Test creating P2pServiceException from an exception without a traceback.
        """
        exception = Exception("Test exception without traceback")
        exc = P2pServiceException.from_service_exception(exception)
        self.assertIsInstance(exc, P2pServiceException)
        self.assertIn("Error handling operation", str(exc))
        self.assertIn("Test exception without traceback", str(exc))
        self.assertIn("line Unknown", str(exc))

    def test_p2p_service_exception_inheritance(self):
        """
        Test that P2pServiceException inherits from P2PException.
        """
        exc = P2pServiceException("Service error")
        self.assertIsInstance(exc, P2PException)
        self.assertEqual(str(exc), "Service error")


if __name__ == "__main__":
    unittest.main()
