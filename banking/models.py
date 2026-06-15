from django.db import models
from customer_management.models import Customer


# Create your models here.


class BankAccountType(models.TextChoices):
    CURRENT = "CURRENT", "Current"
    SAVING = "SAVING", "Saving"


class BankAccountStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class BankAccount(models.Model):
    account_number = models.CharField(
        max_length=200,
        unique=True
    )
    balance = models.FloatField(
        default=0.0
    )
    type = models.CharField(
        max_length=100,
        choices=BankAccountType.choices,
        default=BankAccountType.CURRENT
    )

    status = models.CharField(
        max_length=200,
        choices=BankAccountStatus.choices,
        default=BankAccountStatus.INACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE
    )


class Status(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"


class AccountOpeningRequest(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    account_type = models.CharField(
        max_length=20,
        choices=BankAccountType.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )


class TransactionType(models.TextChoices):
    DEPOSIT = "DEPOSIT", "Deposit"
    WITHDRAW = "WITHDRAW", "Withdraw"
    TRANSFER = "TRANSFER", "Transfer"


class TransactionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"


class TransactionRecord(models.Model):
    type = models.CharField(
        max_length=200,
        choices=TransactionType.choices
    )
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    desc = models.CharField(max_length=200)
    
    source_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE
    )
    destination_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        choices=TransactionStatus.choices
    )
