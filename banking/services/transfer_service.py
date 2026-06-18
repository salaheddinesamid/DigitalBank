from ..models import BankAccount, TransactionRecord

from ..exceptions.insufficent_balance_exception import InsufficientBalanceException
from ..exceptions.blocked_account_exception import AccountBlockedException
from django.db import transaction

from ..utils.check_account_limit import check_daily_limit


def make_internal_transfer(validated_data):
    with transaction.atomic():
        try:
            source_account = BankAccount.objects.get(
                account_number=validated_data['source_account']
            )
        except BankAccount.DoesNotExist:
            raise ValueError("Source account does not exist")

        try:
            destination_account = BankAccount.objects.get(
                account_number=validated_data['destination_account']
            )
        except BankAccount.DoesNotExist:
            raise ValueError("Destination account does not exist")

        # Check if the source account has sufficient balance:
        if source_account.balance < validated_data['amount']:
            raise InsufficientBalanceException("The source account has insufficient balance")

        # Check if the source account is not blocked
        if source_account.status == "BLOCKED":
            raise AccountBlockedException("This account is blocked, you cannot perform any operation")
        check_daily_limit(customer=source_account.customer, amount=validated_data['amount'], transaction_type="TRANSFER")
        # Decrease the source account's balance
        source_account.balance -= validated_data['amount']

        # Increase the destination account's balance
        destination_account.balance += validated_data['amount']

        # Save the accounts
        source_account.save()
        destination_account.save()

        # Create new transaction record:
        transaction_record = TransactionRecord.objects.create(
            type="TRANSFER",
            amount=validated_data['amount'],
            source_account=source_account,
            destination_account=destination_account,
            status="COMPLETED"
        )

        return transaction_record


def make_external_transfer(validated_data):
    pass
