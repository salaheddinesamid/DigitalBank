from ..models import AccountOpeningRequest
from customer_management.models import Customer
from django.db import transaction


@transaction.atomic()
def create_new_account(validated_data):
    try:

        # Create new customer with pending
        new_customer = Customer.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            CIN=validated_data['CIN'],
            phone=validated_data['phone'],
            address=validated_data['address']

        )

        # Create new account request:
        new_account_request = AccountOpeningRequest.objects.create(
            status="PENDING",
            account_type=validated_data['account_type'],
            customer=new_customer
        )

        return new_account_request

    except ValueError:
        raise ValueError()
