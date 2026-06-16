from rest_framework import serializers
from ..models import AccountOpeningRequest, BankAccount


class AccountOpeningRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountOpeningRequest
        fields = '__all__'


class AccountStatusUpdateSerializer(serializers.Serializer):
    status = serializers.CharField()
    request_id = serializers.IntegerField()


class NewAccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
