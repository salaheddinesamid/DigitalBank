from rest_framework import serializers
from ..models import TransactionRecord


class TransactionSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    amount = serializers.FloatField()


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRecord
        fields = '__all__'
