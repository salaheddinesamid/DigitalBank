from django.db import transaction
from ..models import BankAccount, TransactionRecord
from audit.services.create_audit_log import create_audit_log


def make_deposit(validated_data, user, ip_address):
    if validated_data['amount'] <= 0:
        raise ValueError("Deposit amount must be greater than 0")

    with transaction.atomic():
        bank_account = BankAccount.objects.select_for_update().select_related('customer').get(
            customer__user=user
        )

        bank_account.balance += validated_data['amount']
        bank_account.save()

        # Create transaction record for deposit:
        transaction_record = TransactionRecord.objects.create(
            type="DEPOSIT",
            amount=validated_data['amount'],
            destination_account=bank_account,
            status="COMPLETED"
        )

        # Save the transaction record:
        transaction_record.save()

        # Create audit log:
        create_audit_log(
            user=bank_account.customer.user,
            action=transaction_record.type,
            entity="TransactionRecord",
            entity_id=transaction_record.id,
            ip_address=ip_address
        )

    return bank_account
