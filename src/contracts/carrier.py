from typing import Protocol

from messages.requests.collect import CollectRequest
from messages.requests.redirect import RedirectRequest
from messages.responses.information import InformationResponse
from messages.responses.redirect import RedirectResponse
from messages.responses.reverse import ReverseResponse


class Carrier(Protocol):
    def request(self, redirect_request: RedirectRequest) -> RedirectResponse:
        """
        Handle a redirect request.
        """

    def query(self, request_id: str) -> InformationResponse:
        """
        Query a redirect by request ID.
        """

    def collect(self, collect_request: CollectRequest) -> InformationResponse:
        """
        Collect redirect information from a request.
        """

    def reverse(self, transaction_id: str) -> ReverseResponse:
        """
        Reverse a transaction by its ID.
        """
