from django.test import TestCase
from banking.models import AccountOpeningRequest, BankAccount
from customer_management.models import Customer, User
from banking.services.account_approval_service import approve_account_opening_request
from banking.services.deposit_service import make_deposit
from .base_banking_test_case import BaseBankingTestCase


class ApproveAccountOpeningRequestServiceTest(BaseBankingTestCase):

    def test_approve_request_creates_account_and_user(self):
        result = approve_account_opening_request(self.request_obj.id)

        # Refresh from DB
        self.request_obj.refresh_from_db()

        # 1. Request status updated
        self.assertEqual(self.request_obj.status, "APPROVED")

        # 2. Bank account created
        account_exists = BankAccount.objects.filter(
            customer=self.customer
        ).exists()

        self.assertTrue(account_exists)

        account = BankAccount.objects.get(customer=self.customer)

        # 3. Account has valid data
        self.assertIsNotNone(account.account_number)
        self.assertEqual(account.status, "ACTIVE")

        # 4. User created
        user_exists = User.objects.filter(
            username__isnull=False
        ).exists()

        self.assertTrue(user_exists)

        # 5. Service returns something
        self.assertIsNotNone(result)


class BankAccountDepositTest(BaseBankingTestCase):

    def setUp(self):
        super().setUp()

        approve_account_opening_request(self.request_obj.id)

        self.account = BankAccount.objects.get(
            customer=self.customer
        )

    def test_make_deposit(self):
        make_deposit(
            account_number=self.account.account_number,
            amount=500
        )

        self.account.refresh_from_db()

        self.assertEqual(self.account.balance, 500)
