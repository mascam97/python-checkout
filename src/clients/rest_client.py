from typing import Dict

from clients.http_client import HttpClient
from contracts.carrier import Carrier
from entities.settings import Settings
from messages.requests.collect import CollectRequest
from messages.requests.redirect import RedirectRequest
from messages.responses.information import InformationResponse
from messages.responses.redirect import RedirectResponse
from messages.responses.reverse import ReverseResponse


class RestCarrier(Carrier):
    def __init__(self, settings: Settings):
        """
        Initialize the RestCarrier with the given settings.

        :param settings: Settings object with client, authentication, base URL, and logger.
        """
        self.settings = settings
        self.http_client = HttpClient(base_url=settings.base_url, timeout=settings.timeout, logger=settings.logger())

    def _post(self, endpoint: str, arguments: Dict) -> Dict:
        """
        Make an HTTP POST request using the HttpClient.

        :param endpoint: API endpoint.
        :param arguments: Request data.
        :return: Response as a dictionary.
        """
        data = {**arguments, "auth": self.settings.authentication().to_dict()}
        return self.http_client.post(endpoint, json=data, headers=self.settings.additional_headers)

    def request(self, redirect_request: RedirectRequest) -> RedirectResponse:
        """
        Handle a redirect request.
        """
        result = self._post("api/session", redirect_request.to_dict())
        return RedirectResponse(**result)

    def query(self, request_id: str) -> InformationResponse:
        """
        Query a session by request ID.
        """
        result = self._post(f"api/session/{request_id}", {})
        print(result)
        return InformationResponse(**result)

    def collect(self, collect_request: CollectRequest) -> InformationResponse:
        """
        Handle a collect request.
        """
        result = self._post("api/collect", collect_request.to_dict())
        return InformationResponse(**result)

    def reverse(self, transaction_id: str) -> ReverseResponse:
        """
        Reverse a transaction.
        """
        result = self._post("api/reverse", {"internalReference": transaction_id})
        return ReverseResponse(**result)
