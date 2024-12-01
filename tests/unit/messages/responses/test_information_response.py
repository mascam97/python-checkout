import unittest

from entities.status import Status
from entities.subscription_information import SubscriptionInformation
from entities.transaction import Transaction
from enums.status_enum import StatusEnum
from messages.requests.redirect import RedirectRequest
from messages.responses.information import Information


class InformationTest(unittest.TestCase):

    def test_initialization_with_all_fields(self):
        """
        Test initialization of Information with all fields provided.
        """
        status = Status(status=StatusEnum.OK, reason="Request successful")
        request = RedirectRequest(
            locale="en_US",
            return_url="https://example.com/return",
            ip_address="192.168.0.1",
            user_agent="TestAgent",
        )
        transaction = Transaction(
            reference="REF001",
            internal_reference="INT001",
            payment_method="CreditCard",
            payment_method_name="Visa",
            issuer_name="Bank A",
            authorization="AUTH001",
            receipt="REC001",
            franchise="VISA",
            refunded=False,
        )
        subscription = SubscriptionInformation(type="token")

        redirect_info = Information(
            request_id="REQ123",
            status=status,
            request=request,
            payment=[transaction],
            subscription=subscription,
        )

        self.assertEqual(redirect_info.request_id, "REQ123")
        self.assertEqual(redirect_info.status.reason, "Request successful")
        self.assertEqual(redirect_info.request.return_url, "https://example.com/return")
        self.assertEqual(len(redirect_info.payment), 1)
        self.assertEqual(redirect_info.subscription.type, "token")

    def test_initialization_with_defaults(self):
        """
        Test initialization of Information with default values.
        """
        redirect_info = Information(request_id="REQ123")

        self.assertEqual(redirect_info.request_id, "REQ123")
        self.assertIsNone(redirect_info.status)
        self.assertIsNone(redirect_info.request)
        self.assertEqual(redirect_info.payment, [])
        self.assertIsNone(redirect_info.subscription)

    def test_set_payment(self):
        """
        Test setting payment transactions.
        """
        payments_data = [
            {"reference": "REF001", "internalReference": "INT001", "authorization": "AUTH001"},
            {"reference": "REF002", "internalReference": "INT002", "authorization": "AUTH002"},
        ]

        redirect_info = Information(request_id="REQ123")
        redirect_info.set_payment(payments_data)

        self.assertEqual(len(redirect_info.payment), 2)
        self.assertEqual(redirect_info.payment[0].reference, "REF001")
        self.assertEqual(redirect_info.payment[1].reference, "REF002")

    def test_last_transaction(self):
        """
        Test retrieving the last transaction.
        """
        transaction1 = Transaction(reference="REF001", authorization="AUTH001", refunded=False)
        transaction2 = Transaction(reference="REF002", authorization="AUTH002", refunded=False)

        redirect_info = Information(request_id="REQ123", payment=[transaction1, transaction2])

        last_transaction = redirect_info.last_transaction()
        self.assertEqual(last_transaction.reference, "REF002")

    def test_last_approved_transaction(self):
        """
        Test retrieving the last approved transaction.
        """
        status_approved = Status(status=StatusEnum.APPROVED, reason="Approved")
        transaction1 = Transaction(reference="REF001", authorization="AUTH001", refunded=False)
        transaction2 = Transaction(reference="REF002", authorization="AUTH002", refunded=False, status=status_approved)

        redirect_info = Information(request_id="REQ123", payment=[transaction1, transaction2])

        last_approved_transaction = redirect_info.last_approved_transaction()
        self.assertEqual(last_approved_transaction.reference, "REF002")

    def test_last_authorization(self):
        """
        Test retrieving the last authorization.
        """
        status_approved = Status(status=StatusEnum.APPROVED, reason="Approved")
        transaction = Transaction(reference="REF001", authorization="AUTH001", refunded=False, status=status_approved)

        redirect_info = Information(request_id="REQ123", payment=[transaction])

        last_authorization = redirect_info.last_authorization()
        self.assertEqual(last_authorization, "AUTH001")

    def test_to_dict(self):
        """
        Test converting the Information object to a dictionary.
        """
        status = Status(status=StatusEnum.OK, reason="Request successful")
        transaction = Transaction(reference="REF001", authorization="AUTH001")
        subscription = SubscriptionInformation(type="token")

        redirect_info = Information(
            request_id="REQ123",
            status=status,
            payment=[transaction],
            subscription=subscription,
        )

        expected_dict = {
            "requestId": "REQ123",
            "status": status.to_dict(),
            "request": None,
            "payment": [transaction.to_dict()],
            "subscription": subscription.to_dict(),
        }

        self.assertEqual(redirect_info.to_dict(), expected_dict)
