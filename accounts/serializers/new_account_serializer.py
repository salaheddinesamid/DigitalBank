from rest_framework import serializers
from ..models import Customer


class NewAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    CIN = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=200)

    def validate(self, data):

        # Check if the customer already exists
        if Customer.objects.filter(
                CIN=data['CIN']
        ).exists():
            raise serializers.ValidationError("Customer with CIN : {} already exists".format(data['CIN']))
