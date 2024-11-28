from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field

from entities.amount_base import AmountBase


class AmountConversion(BaseModel):
    fromAmount: Optional[AmountBase] = Field(default=None, description="Base amount to convert from")
    toAmount: Optional[AmountBase] = Field(default=None, description="Base amount to convert to")
    factor: float = Field(default=1.0, description="Conversion factor")

    def set_amount_base(self, base: Union[Dict[Any, AmountBase], AmountBase]) -> None:
        """
        Quickly set all values to the same base.

        :param base: Either a dictionary or an instance of AmountBase.
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
            "fromAmount": self.fromAmount.to_dict() if self.fromAmount else None,
            "toAmount": self.toAmount.to_dict() if self.toAmount else None,
            "factor": self.factor,
        }
