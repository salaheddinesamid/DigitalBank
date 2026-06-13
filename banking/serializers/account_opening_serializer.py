from rest_framework import serializers
from ..models import AccountOpeningRequest, BankAccount


class AccountOpeningRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountOpeningRequest
        fields = '__all__'


class NewAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
