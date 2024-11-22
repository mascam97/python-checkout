from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from entities.amount_base import AmountBase


class AmountConversion(BaseModel):
    fromAmount: Optional[AmountBase] = Field(
        default=None, alias="from", description="Base amount to convert from"
    )
    toAmount: Optional[AmountBase] = Field(
        default=None, alias="to", description="Base amount to convert to"
    )
    factor: float = Field(default=1.0, description="Conversion factor")
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    def set_amount_base(self, base: dict) -> None:
        """
        Quickly set all values to the same base.
        """
        amount_base = AmountBase(**base) if isinstance(base, dict) else base
        self.toAmount = amount_base
        self.fromAmount = amount_base
        self.factor = 1.0

    def to_dict(self) -> dict:
        """
        Convert the AmountConversion object to a dictionary.
        """
        return {
            "from": self.fromAmount.to_dict() if self.fromAmount else None,
            "to": self.toAmount.to_dict() if self.toAmount else None,
            "factor": self.factor,
        }
