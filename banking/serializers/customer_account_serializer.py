from rest_framework import serializers
from ..models import BankAccount
from accounts.models import Customer


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerAccountSerializer(serializers.ModelSerializer):
    customer = CustomerDetailsSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = '__all__'
