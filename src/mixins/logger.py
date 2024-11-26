import logging
from typing import Optional, Dict, Any


class Logger:
    """
    A wrapper for logging with dynamic method handling for different log levels.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the Logger instance.

        :param logger: An optional `logging.Logger` instance. If not provided, a default logger is created.
        """
        self.logger = logger or self._create_default_logger()

    def log(self, level: str, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Log a message with the specified level.

        :param level: Log level as a string (e.g., 'debug', 'info').
        :param message: The message to log.
        :param context: Additional context to include in the log.
        """
        if self.logger:
            log_func = getattr(self.logger, level.lower(), self.logger.info)
            context = self.clean_up(context)
            log_func(f"(P2P Checkout) {message} - Context: {context}")

    def __getattr__(self, name: str):
        """
        Dynamically handle logging methods like `debug`, `info`, etc.

        :param name: The name of the method being called.
        :return: A callable function that logs with the specified level.
        """

        def method(message: str, context: Optional[Dict[str, Any]] = None):
            self.log(name, message, context)

        return method

    @staticmethod
    def clean_up(mixed: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Clean up the context by ensuring it's a dictionary.

        :param mixed: The context to clean up.
        :return: A dictionary (empty if input is None or invalid).
        """
        return mixed or {}

    @staticmethod
    def _create_default_logger() -> logging.Logger:
        """
        Create and configure a default logger.

        :return: A `logging.Logger` instance.
        """
        logger = logging.getLogger("P2PLogger")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
