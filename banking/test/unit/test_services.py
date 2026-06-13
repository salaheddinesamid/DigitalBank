from django.test import TestCase
from banking.models import AccountOpeningRequest, BankAccount
from accounts.models import Customer, User
from banking.services.account_approval_service import approve_account_opening_request


class ApproveAccountOpeningRequestServiceTest(TestCase):

    def setUp(self):

        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            CIN="BK123",
            phone="0600000000",
            address="Casa"
        )

        self.request_obj = AccountOpeningRequest.objects.create(
            customer=self.customer,
            account_type="SAVINGS",
            status="PENDING"
        )

    def test_approve_request_creates_account_and_user(self):

        result = approve_account_opening_request(self.request_obj.id)

        # 🔄 Refresh from DB
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