from typing import Optional, Union

from pydantic import BaseModel, Field

from enums.display_on_enum import DisplayOnEnum


class NameValuePair(BaseModel):
    keyword: str = Field(..., description="The keyword associated with the value")
    value: Union[str, list, dict, None] = Field(
        default=None, description="The value, which can be a string, list, or dict"
    )
    displayOn: Optional[DisplayOnEnum] = Field(
        default=DisplayOnEnum.NONE, description="Display setting for the keyword"
    )

    def to_dict(self) -> dict:
        """
        Convert the NameValuePair object to a dictionary using the Pydantic `model_dump` method.
        """
        return self.model_dump()
