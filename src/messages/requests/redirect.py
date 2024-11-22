from typing import Optional
from pydantic import BaseModel, Field
from entities.person import Person
from entities.dispersion_payment import DispersionPayment
from entities.subscription import Subscription


class RedirectRequest(BaseModel):
    locale: str = Field(default="es_CO", description="Locale of the request")
    payer: Optional[Person] = Field(
        default=None, description="Information about the payer"
    )
    buyer: Optional[Person] = Field(
        default=None, description="Information about the buyer"
    )
    payment: Optional[DispersionPayment] = Field(
        default=None, description="Payment details"
    )
    subscription: Optional[Subscription] = Field(
        default=None, description="Subscription details"
    )
    return_url: str = Field(..., description="URL to return to after processing")
    payment_method: str = Field(default="", description="Payment method to be used")
    cancel_url: str = Field(default="", description="URL to return to if canceled")
    ip_address: str = Field(..., description="IP address of the user")
    user_agent: str = Field(..., description="User agent of the user's browser")
    expiration: str = Field(default=None, description="Expiration date for the request")
    capture_address: bool = Field(
        default=False, description="Whether to capture the address"
    )
    skip_result: bool = Field(
        default=False, description="Whether to skip showing results"
    )
    no_buyer_fill: bool = Field(
        default=False, description="Whether to avoid pre-filling buyer data"
    )

    @staticmethod
    def from_dict(data: dict) -> "RedirectRequest":

        return RedirectRequest(**data)
