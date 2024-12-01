from typing import Any, Dict, Type, TypeVar, Union

from entities.settings import Settings
from exceptions.p2p_exception import P2PException
from messages.requests.collect import CollectRequest
from messages.requests.redirect import RedirectRequest
from messages.responses.information import Information
from messages.responses.redirect import RedirectResponse
from messages.responses.reverse import ReverseResponse

T = TypeVar("T", RedirectRequest, CollectRequest)


class P2PCheckout:
    """
    Main class for interacting with PlaceToPay.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the PlacetoPay instance with the provided settings.

        :param data: Configuration dictionary for settings.
        """
        self.settings: Settings = Settings(**data)

    def _validate_request(self, request: Union[RedirectRequest, CollectRequest, Dict], expected_class: Type[T]) -> T:
        """
        Validate the request object and convert it to the expected class if necessary.

        :param request: The request object or dictionary.
        :param expected_class: The expected class type for the request.
        :return: A validated request object.
        :raises P2PException: If the request is invalid.
        """
        if isinstance(request, dict):
            request = expected_class(**request)

        if not isinstance(request, expected_class):
            raise P2PException.for_data_not_provided(f"Invalid request type. Expected {expected_class.__name__}")

        return request

    def request(self, redirect_request: Union[RedirectRequest, Dict]) -> RedirectResponse:
        """
        Handle a redirect request.

        :param redirect_request: RedirectRequest instance or dictionary with request data.
        :return: RedirectResponse object.
        """
        redirect_request = self._validate_request(redirect_request, RedirectRequest)
        return self.settings.carrier().request(redirect_request)

    def query(self, request_id: str) -> Information:
        """
        Query a session by request ID.

        :param request_id: The ID of the request to query.
        :return: RedirectInformation object.
        """
        return self.settings.carrier().query(request_id)

    def collect(self, collect_request: Union[CollectRequest, Dict]) -> Information:
        """
        Handle a collect request.

        :param collect_request: CollectRequest instance or dictionary with request data.
        :return: RedirectInformation object.
        """
        collect_request = self._validate_request(collect_request, CollectRequest)
        return self.settings.carrier().collect(collect_request)

    def reverse(self, internal_reference: str) -> ReverseResponse:
        """
        Reverse a transaction.

        :param internal_reference: The internal reference of the transaction to reverse.
        :return: ReverseResponse object.
        """
        return self.settings.carrier().reverse(internal_reference)
