from typing import List, Optional, Union

from pydantic import BaseModel, Field

from entities.account import Account
from entities.name_value_pair import NameValuePair
from entities.status import Status
from entities.token import Token


class SubscriptionInformation(BaseModel):
    type: str = Field(
        default="", description="Type of subscription (e.g., token, account)"
    )
    status: Optional[Status] = Field(
        default=None, description="Status information")
    instrument: List[NameValuePair] = Field(
        default_factory=list, description="Instrument details as name-value pairs"
    )

    def set_instrument(self, instrument_data: Union[dict, List[dict]]) -> None:
        """
        Set the instrument data as a list of NameValuePair objects.
        """
        self.instrument = []
        if isinstance(instrument_data, dict) and "item" in instrument_data:
            instrument_data = instrument_data["item"]

        for nvp_data in instrument_data:
            if isinstance(nvp_data, dict):
                nvp_data = NameValuePair(**nvp_data)
            if isinstance(nvp_data, NameValuePair):
                self.instrument.append(nvp_data)

    def instrument_to_list(self) -> List[dict]:
        """
        Convert the instrument to a list of dictionaries.
        """
        return [nvp.to_dict() for nvp in self.instrument]

    def parse_instrument(self) -> Optional[Union[Account, Token]]:
        """
        Parse the instrument as the proper entity (Account or Token) or return None.
        """
        if not self.instrument:
            return None

        data = {"status": self.status.to_dict() if self.status else None}
        for nvp in self.instrument:
            data[nvp.keyword] = nvp.value

        if self.type == "token":
            return Token(**data)
        elif self.type == "account":
            return Account(**data)
        return None

    def to_dict(self) -> dict:
        """
        Convert the SubscriptionInformation object to a dictionary.
        """
        return {
            "type": self.type,
            "status": self.status.to_dict() if self.status else None,
            "instrument": self.instrument_to_list(),
        }
