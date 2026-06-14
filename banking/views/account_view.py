from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

# import models
from ..models import BankAccount

# import serializers
from ..serializers.customer_account_serializer import CustomerAccountSerializer
from ..serializers.new_account_serializer import NewAccountSerializer
from ..serializers.account_opening_serializer import AccountOpeningRequestSerializer

# import services
from ..services.new_account_service import create_new_account


class AccountDetailViewSet(ViewSet):

    @action(detail=True, methods=["get"])
    def get_details(self, request):
        account_number = request.query_params.get('number')
        account = BankAccount.objects.select_related('customer').get(
            account_number=account_number
        )

        serializer = CustomerAccountSerializer(account)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["patch"])
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

    @action(detail=True, methods=["patch"])
    def update_status(self, request):
        pass
