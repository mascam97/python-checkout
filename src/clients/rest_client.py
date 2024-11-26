import requests
from typing import Dict
from entities.settings import Settings
from contracts.carrier import Carrier
from exceptions.p2p_exception import P2PException
from exceptions.p2p_service_exception import P2pServiceException
from messages.requests.collect import CollectRequest
from messages.requests.redirect import RedirectRequest
from messages.responses.information import RedirectInformation
from messages.responses.redirect import RedirectResponse
from messages.responses.reverse import ReverseResponse


class RestCarrier(Carrier):
    def __init__(self, settings: Settings):
        """
        Initialize the RestCarrier with the given settings.

        :param settings: Settings object with client, authentication, base URL, and logger.
        """
        self.settings = settings

    def request(self, redirect_request: RedirectRequest) -> RedirectResponse:
        """
        Handle a redirect request.

        :param redirect_request: RedirectRequest object containing the request data.
        :return: RedirectResponse object.
        """
        result = self._post("api/session", redirect_request.to_dict())
        return RedirectResponse(**result)

    def query(self, request_id: str) -> RedirectInformation:
        """
        Query a session by request ID.

        :param request_id: The ID of the request to query.
        :return: RedirectInformation object.
        """
        result = self._post(f"api/session/{request_id}", {})
        return RedirectInformation(**result)

    def collect(self, collect_request: CollectRequest) -> RedirectInformation:
        """
        Handle a collect request.

        :param collect_request: CollectRequest object containing the request data.
        :return: RedirectInformation object.
        """
        result = self._post("api/collect", collect_request.to_dict())
        return RedirectInformation(**result)

    def reverse(self, transaction_id: str) -> ReverseResponse:
        """
        Reverse a transaction.

        :param transaction_id: The ID of the transaction to reverse.
        :return: ReverseResponse object.
        """
        result = self._post(
            "api/reverse", {"internalReference": transaction_id})
        return ReverseResponse(**result)

    def _post(self, endpoint: str, arguments: Dict) -> Dict:
        url = self.settings.base_url_with_endpoint(endpoint)
        """
        Make an HTTP POST request to the specified URL with the given arguments.

        :param url: The URL to send the request to.
        :param arguments: The data to include in the request.
        :return: Parsed JSON response as a dictionary.
        :raises P2pServiceException: If an unexpected error occurs.
        """
        try:
            data = {**arguments, "auth": self.settings.authentication().to_dict()}
            self.settings.logger().debug("REQUEST", data)
            response = self.settings.client().post(
                url, json=data, headers=self.settings.headers()
            )

            self.settings.logger().debug("RESPONSE", {"result": response.text})
            return response.json()
        except requests.exceptions.RequestException as e:
            if e.response is not None:
                self.settings.logger().warning(
                    "BAD_RESPONSE",
                    {"class": type(e).__name__, "result": e.response.text},
                )
            else:
                self.settings.logger().warning(
                    "BAD_RESPONSE", {"class": type(e).__name__}
                )
            raise P2PException.for_data_not_provided(f"Request failed: {e}")
        except Exception as e:
            self.settings.logger().warning(
                "EXCEPTION_RESPONSE",
                {"exception": P2PException.read_exception(e)},
            )
            raise P2pServiceException.from_service_exception(e)
