from typing import Any, Dict, Type, TypeVar, Union

from contracts.carrier import Carrier
from entities.settings import Settings
from exceptions.p2p_exception import P2PException
from exceptions.p2p_service_exception import P2pServiceException
from messages.requests.collect import CollectRequest
from messages.requests.redirect import RedirectRequest
from messages.responses.information import InformationResponse
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
        self.logger = self.settings.logger()

    def _validate_request(self, request: Union[RedirectRequest, CollectRequest, Dict], expected_class: Type[T]) -> T:
        """
        Validate the request object and convert it to the expected class if necessary.

        :param request: The request object or dictionary.
        :param expected_class: The expected class type for the request.
        :return: A validated request object.
        :raises P2PException: If the request is invalid.
        """
        if isinstance(request, dict):
            try:
                request = expected_class(**request)
            except Exception as e:
                self.logger.error(f"Failed to convert dictionary to {expected_class.__name__}: {e}")
                raise P2PException.for_data_not_provided(
                    f"Failed to convert dictionary to {expected_class.__name__}: {e}"
                )

        if not isinstance(request, expected_class):
            self.logger.error(f"Invalid request type: {type(request).__name__}. Expected {expected_class.__name__}.")
            raise P2PException.for_data_not_provided(
                f"Invalid request type: {type(request).__name__}. Expected {expected_class.__name__}."
            )

        self.logger.debug(f"Request validated as {expected_class.__name__}.")
        return request

    @property
    def carrier(self) -> Carrier:
        """
        Access the carrier instance from settings.
        """
        return self.settings.carrier()

    def request(self, redirect_request: Union[RedirectRequest, Dict]) -> RedirectResponse:
        """
        Handle a redirect request.

        :param redirect_request: RedirectRequest instance or dictionary with request data.
        :return: RedirectResponse object.
        """
        redirect_request = self._validate_request(redirect_request, RedirectRequest)
        return self.carrier.request(redirect_request)

    def query(self, request_id: str) -> InformationResponse:
        """
        Query a session by request ID.

        :param request_id: The ID of the request to query.
        :return: Information object.
        """
        self.logger.info(f"Querying request ID: {request_id}.")
        return self.carrier.query(request_id)

    def collect(self, collect_request: Union[CollectRequest, Dict]) -> InformationResponse:
        """
        Handle a collect request.

        :param collect_request: CollectRequest instance or dictionary with request data.
        :return: Information object.
        """
        collect_request = self._validate_request(collect_request, CollectRequest)
        try:
            response = self.carrier.collect(collect_request)
            return response
        except Exception as e:
            self.logger.error(f"Error during collect request: {e}")
            raise P2pServiceException.from_service_exception(e)

    def reverse(self, internal_reference: str) -> ReverseResponse:
        """
        Reverse a transaction.

        :param internal_reference: The internal reference of the transaction to reverse.
        :return: ReverseResponse object.
        """
        self.logger.info(f"Reversing transaction with reference: {internal_reference}.")
        try:
            return self.carrier.reverse(internal_reference)
        except Exception as e:
            self.logger.error(f"Error during reversal for reference {internal_reference}: {e}")
            raise P2pServiceException.from_service_exception(e)
