from ..models import AccountOpeningRequest, BankAccount
from accounts.models import User, Customer, Role
from ..utils.account_number_generator import generate_account_number
from ..utils.user_credentials_generator import generate_user_credentials
from django.db import transaction


@transaction.atomic()
def approve_account_opening_request(request_id):
    # Fetch the opening request
    opening_request = AccountOpeningRequest.objects.get(
        id=request_id
    )
    # Verify the status
    if opening_request.status != "PENDING":
        raise ValueError("Your account opening request is already accepted or rejected")

    # Fetch the customer details
    customer = opening_request.customer

    # Update the status of the request
    opening_request.status = "APPROVED"
    opening_request.save()

    # Create new user credentials
    user_credentials = generate_user_credentials(
        first_name=customer.first_name,
        last_name=customer.last_name,
        CIN=customer.CIN
    )
    new_user = User.objects.create(
        username=user_credentials['username']
    )

    # Fetch the customer role from DB:
    customer_role = Role.objects.get(
        role_name="CUSTOMER"
    )
    # Add the customer role to the user:
    new_user.roles.add(customer_role)

    # Set a hashed password to the user
    new_user.set_password(
        user_credentials['password']
    )
    # Save the user
    new_user.save()

    # Link the customer with user credentials
    customer.user = new_user
    customer.save()

    # Create new account
    banking_account = BankAccount.objects.create(
        account_number=generate_account_number(
            id=new_user.id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            CIN=customer.CIN
        ),
        balance=0.0,
        type=opening_request.account_type,
        status="ACTIVE",
        customer=customer
    )

    return banking_account
