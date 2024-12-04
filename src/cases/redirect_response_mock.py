from functools import wraps
import json
from typing import Any, Callable, Dict


class RedirectResponseMock:
    @staticmethod
    def get_mock_response(file_name: str, status_code: int) -> Dict[str, Any]:
        """
        Load mock response data from a file and return it with headers for a given status code.

        :param file_name: Name of the file containing the mock response.
        :param status_code: HTTP status code to determine the headers.
        :return: A dictionary containing the response body and headers.
        """
        file_path = f"tests/mocks/responses/{file_name}.json"
        with open(file_path, "r") as file:
            body = json.load(file)

        headers = {
            200: {
                "Content-Type": "application/json",
                "X-Mock-Status": "Success",
            },
            400: {
                "Content-Type": "application/json",
                "X-Mock-Status": "Bad Request",
            },
        }.get(status_code, {"Content-Type": "application/json"})

        return {"body": body, "headers": headers}

    @staticmethod
    def mock_response_decorator(
        file_name: str, status_code: int = 200
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        A decorator that injects a mock response into the test function.

        :param file_name: Name of the file containing the mock response.
        :param status_code: HTTP status code to determine the headers (default: 200).
        :return: A decorator function that modifies the test function to include the mock response.
        """

        def decorator(test_func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(test_func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                mock_response = RedirectResponseMock.get_mock_response(file_name, status_code)
                return test_func(*args, mock_response=mock_response, **kwargs)

            return wrapper

        return decorator
