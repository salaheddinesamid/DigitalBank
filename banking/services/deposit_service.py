from django.db import transaction
from ..models import BankAccount


def make_deposit(validated_data):
    if validated_data['amount'] <= 0:
        raise ValueError("Deposit amount must be greater than 0")

    with transaction.atomic():
        bank_account = BankAccount.objects.select_for_update().get(
            account_number=validated_data['account_number']
        )

        bank_account.balance += validated_data['amount']
        bank_account.save()

    return bank_account
