from django.test import TestCase

from banking.models import AccountOpeningRequest, BankAccount
from customer_management.models import Customer


class BaseBankingTestCase(TestCase):

    def setUp(self):

        # Define customer objects:
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            CIN="BK123",
            phone="0600000000",
            address="Casa"
        )

        self.customer2 = Customer.objects.create(
            first_name="Salaheddine",
            last_name="Samid",
            CIN="OLM123",
            phone="0600000000",
            address="Casablanca"
        )

        # Define customer bank accounts
        self.customer_bank_account = BankAccount.objects.create(
            customer=self.customer,
            account_number="DDKL098",
            balance=9000.0,
            type="CURRENT"
        )

        self.customer2_bank_account = BankAccount.objects.create(
            customer=self.customer2,
            account_number="FBHL098",
            balance=9000.0,
            type="CURRENT"
        )

        self.request_obj = AccountOpeningRequest.objects.create(
            customer=self.customer,
            account_type="SAVING",
            status="PENDING"
        )