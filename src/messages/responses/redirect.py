from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from entities.status import Status


class RedirectResponse(BaseModel):
    request_id: str = Field(
        default="",
        alias="requestId",
        description="Unique transaction code for this request",
    )
    session_url: str = Field(
        default="",
        alias="session_url",
        description="URL to consume when the gateway requires redirection",
    )
    status: Optional[Status] = Field(..., description="Status of the transaction")
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    def is_successful(self) -> bool:
        """
        Check if the status is successful (OK).
        """
        return self.status.is_successful() if self.status else False

    def to_dict(self) -> dict:
        """
        Convert the RedirectResponse object to a dictionary.
        """
        return self.model_dump(by_alias=True, exclude_none=True)
