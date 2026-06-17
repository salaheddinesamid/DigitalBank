from rest_framework import serializers
from ..models import TransactionRecord


class TransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRecord
        fields = '__all__'

