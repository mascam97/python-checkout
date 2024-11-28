from typing import Optional

from pydantic import BaseModel, Field

from entities.dispersion_payment import DispersionPayment
from entities.person import Person
from entities.subscription import Subscription


class RedirectRequest(BaseModel):
    locale: str = Field(default="es_CO", description="Locale of the request", alias="locale")
    payer: Optional[Person] = Field(default=None, description="Information about the payer", alias="payer")
    buyer: Optional[Person] = Field(default=None, description="Information about the buyer", alias="buyer")
    payment: Optional[DispersionPayment] = Field(default=None, description="Payment details", alias="payment")
    subscription: Optional[Subscription] = Field(default=None, description="Subscription details", alias="subscription")
    return_url: str = Field(..., description="URL to return to after processing", alias="returnUrl")
    payment_method: str = Field(default="", description="Payment method to be used", alias="paymentMethod")
    cancel_url: str = Field(default="", description="URL to return to if canceled", alias="cancelUrl")
    ip_address: str = Field(..., description="IP address of the user", alias="ipAddress")
    user_agent: str = Field(..., description="User agent of the user's browser", alias="userAgent")
    expiration: Optional[str] = Field(default=None, description="Expiration date for the request", alias="expiration")
    capture_address: bool = Field(default=False, description="Whether to capture the address", alias="captureAddress")
    skip_result: bool = Field(default=False, description="Whether to skip showing results", alias="skipResult")
    no_buyer_fill: bool = Field(
        default=False, description="Whether to avoid pre-filling buyer data", alias="noBuyerFill"
    )

    @staticmethod
    def from_dict(data: dict) -> "RedirectRequest":
        """
        Create an instance of RedirectRequest from a dictionary.
        """
        return RedirectRequest(**data)

    def to_dict(self) -> dict:
        """
        Convert the RedirectRequest object to a dictionary using Pydantic's dict method.
        """
        return self.model_dump(by_alias=True, exclude_none=True)
