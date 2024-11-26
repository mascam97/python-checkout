from typing import Union, Any
from pydantic import BaseModel, Field


class NameValuePair(BaseModel):
    keyword: str = Field(...,
                         description="The keyword associated with the value")
    value: Union[str, list, dict, None] = Field(
        default=None, description="The value, which can be a string, list, or dict"
    )
    displayOn: str = Field(
        default="none", description="Display setting for the keyword")

    def to_dict(self) -> dict:
        """
        Convert the NameValuePair object to a dictionary using the Pydantic `model_dump` method.
        """
        return self.model_dump(exclude_none=True)
