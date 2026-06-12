from rest_framework import serializers
from ..models import AccountOpeningRequest


class AccountOpeningRequestSerializer(serializers.ModelSerializer):
    model = AccountOpeningRequest
    fields = '__all__'
