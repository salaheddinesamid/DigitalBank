from django.db import transaction
from ..models import BankAccount


def make_deposit(account_number, amount):
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than 0")

    with transaction.atomic():
        bank_account = BankAccount.objects.select_for_update().get(
            account_number=account_number
        )

        bank_account.balance += amount
        bank_account.save()

    return bank_account
