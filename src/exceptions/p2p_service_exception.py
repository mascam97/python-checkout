from p2p_exception import P2PException


class P2pServiceException(P2PException):
    """
    Exception class for handling errors from PlaceToPay services.
    """

    @staticmethod
    def from_service_exception(exception: Exception) -> "P2pServiceException":
        """
        Create a new PlacetoPayServiceException from another exception.

        :param exception: The original exception that caused the service error.
        :return: A new instance of PlacetoPayServiceException.
        """
        return P2pServiceException(
            "Error handling operation",
            exception.__traceback__.tb_lineno,
        )
