from django.db import models
from rest_framework import serializers
from ..models import BankAccount, TransactionRecord
from customer_management.models import Customer


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class RecentTransactionSerializer(serializers.ModelSerializer):
    source_account = serializers.CharField(
        source="source_account.account_number",
        read_only=True
    )

    destination_account = serializers.CharField(
        source="destination_account.account_number",
        read_only=True
    )

    class Meta:
        model = TransactionRecord

        fields = [
            "id",
            "type",
            "amount",
            "status",
            "source_account",
            "destination_account",
            "timestamp"
        ]


class CustomerAccountSerializer(serializers.ModelSerializer):
    customer = CustomerDetailsSerializer(
        read_only=True
    )

    recent_transactions = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount

        fields = [
            "id",
            "account_number",
            "type",
            "balance",
            "status",
            "customer",
            "recent_transactions"
        ]

    def get_recent_transactions(self, account):
        transactions = TransactionRecord.objects.filter(
            models.Q(source_account=account) |
            models.Q(destination_account=account)
        ).order_by(
            "-timestamp"
        )[:5]

        return RecentTransactionSerializer(
            transactions,
            many=True
        ).data
