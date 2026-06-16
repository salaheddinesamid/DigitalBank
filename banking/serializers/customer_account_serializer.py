from rest_framework import serializers
from ..models import BankAccount
from customer_management.models import Customer


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class CustomerAccountSerializer(serializers.ModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)
    bank_account = CustomerBankAccountSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = '__all__'
