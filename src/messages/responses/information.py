from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from entities.status import Status
from entities.subscription_information import SubscriptionInformation
from entities.transaction import Transaction
from messages.requests.redirect import RedirectRequest


class RedirectInformation(BaseModel):
    request_id: str = Field(
        ..., alias="requestId", description="Unique identifier for the request"
    )
    status: Optional[Status] = Field(
        default=None, description="Status of the request")
    request: Optional[RedirectRequest] = Field(
        default=None, description="Redirect request details"
    )
    payment: List[Transaction] = Field(
        default_factory=list, description="List of payment transactions"
    )
    subscription: Optional[SubscriptionInformation] = Field(
        default=None, description="Subscription details"
    )
    model_config = ConfigDict(
        arbitrary_types_allowed=True, populate_by_name=True)

    def set_payment(self, payments: List[dict]) -> None:
        """
        Set the payment transactions.
        """
        if payments:
            self.payment = []
            if isinstance(payments, dict) and "transaction" in payments:
                payments = payments["transaction"]

            for payment_data in payments:
                self.payment.append(Transaction(**payment_data))

    def last_transaction(self, approved: bool = False) -> Optional[Transaction]:
        """
        Get the last transaction made in the session.
        If approved is True, returns the last approved transaction.
        """
        if not self.payment:
            return None

        if approved:
            for transaction in self.payment:
                if transaction.is_approved():
                    return transaction
        return self.payment[-1] if self.payment else None

    def last_approved_transaction(self) -> Optional[Transaction]:
        """
        Get the last approved transaction.
        """
        return self.last_transaction(approved=True)

    def last_authorization(self) -> str:
        """
        Returns the last authorization associated with the session.
        """
        last_approved = self.last_approved_transaction()
        return last_approved.authorization if last_approved else ""

    def to_dict(self) -> dict:
        """
        Convert the RedirectInformation object to a dictionary.
        """
        return {
            "requestId": self.request_id,
            "status": self.status.to_dict() if self.status else None,
            "request": self.request.to_dict() if self.request else None,
            "payment": [transaction.to_dict() for transaction in self.payment],
            "subscription": self.subscription.to_dict() if self.subscription else None,
        }
