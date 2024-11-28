from exceptions.p2p_exception import P2PException


class P2pServiceException(P2PException):
    """
    Exception class for handling errors from PlaceToPay services.
    """

    @staticmethod
    def from_service_exception(exception: Exception) -> "P2pServiceException":
        """
        Create a new P2pServiceException from another exception.

        :param exception: The original exception that caused the service error.
        :return: A new instance of P2pServiceException.
        """
        line_number = (
            exception.__traceback__.tb_lineno if exception.__traceback__ else "Unknown"
        )
        return P2pServiceException(
            f"Error handling operation: {exception} (line {line_number})"
        )
