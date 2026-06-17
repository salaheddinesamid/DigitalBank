from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

# import models
from ..models import BankAccount
from customer_management.models import Customer, User

# import serializers
from ..serializers.customer_account_serializer import CustomerAccountSerializer
from ..serializers.new_account_serializer import NewAccountSerializer
from ..serializers.account_opening_serializer import AccountOpeningRequestSerializer, AccountStatusUpdateSerializer, NewAccountDetailsSerializer

# import services
from ..services.new_account_service import create_new_account
from ..services.account_approval_service import approve_account_opening_request

# Import permissions
from DigitalBank.security.permissions import IsCustomer


class AccountDetailViewSet(ViewSet):

    @action(detail=False, methods=["get"], permission_classes=[IsCustomer])
    def get_details(self, request):

        # Fetch the customer
        user = request.user
        account = BankAccount.objects.select_related('customer').get(
            customer__user=user
        )

        serializer = CustomerAccountSerializer(account)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def create_new_account(self, request):
        serializer = NewAccountSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        opening_request = create_new_account(
            serializer.validated_data
        )

        response_serializer = AccountOpeningRequestSerializer(
            opening_request
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["patch"])
    def update_status(self, request):

        try:

            serializer = AccountStatusUpdateSerializer(
                data=request.data
            )

            serializer.is_valid(
                raise_exception=True
            )

            request_id = serializer.validated_data[
                'request_id'
            ]

            status_value = serializer.validated_data[
                'status'
            ]

            if status_value == "APPROVED":
                updated_account = (
                    approve_account_opening_request(
                        request_id=request_id
                    )
                )

                response_serializer = (
                    NewAccountDetailsSerializer(
                        updated_account
                    )
                )

                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    "error": "Unsupported status"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
