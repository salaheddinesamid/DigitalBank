from django.test import TestCase

from banking.models import AccountOpeningRequest, BankAccount
from customer_management.models import Customer


class BaseBankingTestCase(TestCase):

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
            account_type="SAVING",
            status="PENDING"
        )