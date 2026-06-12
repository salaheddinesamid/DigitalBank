from rest_framework import serializers
from ..models import AccountOpeningRequest


class AccountOpeningRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountOpeningRequest
        fields = '__all__'
