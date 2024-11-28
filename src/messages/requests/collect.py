from typing import Optional
from pydantic import Field
from messages.requests.redirect import RedirectRequest
from entities.instrument import Instrument


class CollectRequest(RedirectRequest):
    instrument: Optional[Instrument] = Field(...,
                                             description="Instrument details")
    return_url: str = Field(
        default="", alias="returnUrl", description="URL to return to after processing"
    )
    ip_address: str = Field(
        default="", alias="ipAddress", description="IP address of the user"
    )
    user_agent: str = Field(
        default="", alias="userAgent", description="User agent of the user's browser"
    )

    def to_dict(self) -> dict:
        """
        Convert the CollectRequest object to a dictionary.
        """
        parent_dict = super().model_dump()
        return {
            **parent_dict,
            "instrument": self.instrument.to_dict() if self.instrument else None,
        }
