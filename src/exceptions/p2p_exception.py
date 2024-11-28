from typing import Optional


class P2PException(Exception):
    """
    Custom exception class for PlaceToPay errors.
    """

    @staticmethod
    def read_exception(exception: Exception) -> str:
        """
        Return a detailed string representation of an exception.

        :param exception: The exception to read.
        :return: A string containing the message, file, line, and class of the exception.
        """
        if exception.__traceback__ is not None:
            return (
                f"{exception} ON {exception.__traceback__.tb_frame.f_code.co_filename} "
                f"LINE {exception.__traceback__.tb_lineno} [{exception.__class__.__name__}]"
            )
        return f"{exception} [No traceback available]"

    @staticmethod
    def for_data_not_provided(message: Optional[str] = "") -> "P2PException":
        """
        Return a new P2PException for missing data errors.

        :param message: The error message.
        :return: A new instance of P2PException.
        """
        return P2PException(message)
