from ..models import BankAccount, TransactionRecord
from ..exceptions.insufficent_balance_exception import InsufficientBalanceException
from customer_management.exceptions.inactive_account_exception import InactiveBankAccountException
from django.db import transaction


def make_withdraw(validate_data):
    if validate_data['amount'] < 0:
        raise ValueError("Please enter a positive value")

    with transaction.atomic():
        bank_account = BankAccount.objects.select_for_update().get(
            account_number=validate_data['account_number']
        )

        # If the account is inactive, raise an exception
        if bank_account.status == "INACTIVE":
            raise InactiveBankAccountException('This account is inactive, please activate your account and try again')

        # If the account is out of balance, raise an exception
        if validate_data['amount'] > bank_account.balance:
            raise InsufficientBalanceException('Insufficient balance, please try again')

        # Otherwise, update:
        bank_account.balance -= validate_data['amount']
        bank_account.save()

        # Create transaction record for withdraw:
        transaction_record = TransactionRecord.objects.create(
            type="WITHDRAW",
            amount=validate_data['amount'],
            source_account=bank_account,
            status="PENDING"
        )

        # Save the transaction record
        transaction_record.save()

    return bank_account
