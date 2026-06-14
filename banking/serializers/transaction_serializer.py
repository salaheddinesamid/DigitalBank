from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    amount = serializers.FloatField()