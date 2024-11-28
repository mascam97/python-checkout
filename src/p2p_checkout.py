from typing import Any, Dict, Union

from entities.settings import Settings
from exceptions.p2p_exception import P2PException
from messages.requests.collect import CollectRequest
from messages.requests.redirect import RedirectRequest
from messages.responses.information import RedirectInformation
from messages.responses.redirect import RedirectResponse
from messages.responses.reverse import ReverseResponse


class P2PCheckout:
    """
    Main class for interacting with PlaceToPay.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize the PlacetoPay instance with the provided settings.

        :param data: Configuration dictionary for settings.
        """
        self.settings = Settings(**data)

    def request(
        self, redirect_request: Union[RedirectRequest, Dict]
    ) -> RedirectResponse:
        """
        Handle a redirect request.

        :param redirect_request: RedirectRequest instance or dictionary with request data.
        :return: RedirectResponse object.
        :raises P2PException: If the request object is invalid.
        """
        if isinstance(redirect_request, dict):
            redirect_request = RedirectRequest(**redirect_request)

        if not isinstance(redirect_request, RedirectRequest):
            raise P2PException.for_data_not_provided("Wrong class request")

        return self.settings.carrier().request(redirect_request)

    def query(self, request_id: int) -> RedirectInformation:
        """
        Query a session by request ID.

        :param request_id: The ID of the request to query.
        :return: RedirectInformation object.
        """
        return self.settings.carrier().query(request_id)

    def collect(
        self, collect_request: Union[CollectRequest, Dict]
    ) -> RedirectInformation:
        """
        Handle a collect request.

        :param collect_request: CollectRequest instance or dictionary with request data.
        :return: RedirectInformation object.
        :raises P2PException: If the collect request object is invalid.
        """
        if isinstance(collect_request, dict):
            collect_request = CollectRequest(**collect_request)

        if not isinstance(collect_request, CollectRequest):
            raise P2PException("Wrong collect request")

        return self.settings.carrier().collect(collect_request)

    def reverse(self, internal_reference: str) -> ReverseResponse:
        """
        Reverse a transaction.

        :param internal_reference: The internal reference of the transaction to reverse.
        :return: ReverseResponse object.
        """
        return self.settings.carrier().reverse(internal_reference)
