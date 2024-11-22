class BaseException(Exception):
    """
    Base class for API-related exceptions.
    """

    def __init__(self, message: str, status_code: int = None, details: dict = None):
        """
        Initialize the API exception.

        :param message: Description of the error.
        :param status_code: HTTP status code associated with the error (if applicable).
        :param details: Additional details about the error (e.g., error codes, metadata).
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> dict:
        """
        Convert the exception details to a dictionary for serialization.
        """
        return {
            "error": self.message,
            "status_code": self.status_code,
            "details": self.details,
        }

    def __str__(self) -> str:
        """
        String representation of the exception.
        """
        base_message = (
            f"{self.message} (Status Code: {self.status_code})"
            if self.status_code
            else self.message
        )
        if self.details:
            base_message += f" | Details: {self.details}"
        return base_message
