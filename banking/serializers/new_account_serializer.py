from rest_framework import serializers
from ..models import Customer


class NewAccountSerializer(serializers.Serializer):
    valid_account_types = ("CURRENT", "SAVING")
    # Customer information
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    CIN = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=200)

    # Banking account details:
    account_type = serializers.CharField()

    def validate(self, data):
        # Check if the account type is valid
        if data['account_type'] not in self.valid_account_types:
            raise serializers.ValidationError("Please select the right account type.")
        # Check if the customer already exists
        if Customer.objects.filter(
                CIN=data['CIN']
        ).exists():
            raise serializers.ValidationError("Customer with CIN : {} already exists".format(data['CIN']))

        return data
