from django.db.models import Sum
from django.utils import timezone

from ..models import TransactionRecord


def check_daily_limit(customer, amount, transaction_type):
    today = timezone.now().date()
    total_transaction_amount = TransactionRecord.objects.filter(
        source_account__customer=customer,
        type=transaction_type,
        timestamp__day=today
    ).aggregate(
        total=Sum("amount")
    )['total'] or 0

    limit = customer.bankaccount.daily_limit

    if total_transaction_amount + amount > limit:
        raise ValueError(
            "Daily transfer limit exceeded"
        )


def check_monthly_limit(customer, amount):
    pass
