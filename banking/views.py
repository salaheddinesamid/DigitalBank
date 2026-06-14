from django.shortcuts import render
from rest_framework.views import APIView
from .serializers.new_account_serializer import NewAccountSerializer
from .serializers.account_opening_serializer import AccountOpeningRequestSerializer
from .services.new_account_service import create_new_account
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers.new_account_serializer import NewAccountSerializer
from .serializers.account_opening_serializer import AccountOpeningRequestSerializer, NewAccountDetailsSerializer
from .services.new_account_service import create_new_account
from .serializers.customer_account_serializer import CustomerAccountSerializer
from .services.account_approval_service import approve_account_opening_request
from .services.deposit_service import make_deposit
from .services.withdraw_service import make_withdraw
from .models import AccountOpeningRequest, BankAccount
from .exceptions.insufficent_balance_exception import InsufficientBalanceException
from customer_management.exceptions.inactive_account_exception import InactiveBankAccountException


class AccountCreationView(APIView):

    def post(self, request):
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


class AccountOpeningRequestUpdate(APIView):

    def post(self, request, pk):
        try:
            banking_account = approve_account_opening_request(
                request_id=pk
            )
            serializer = NewAccountDetailsSerializer(banking_account)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except ValueError:
            return Response(
                data={
                    'error': 'This opening request may have already been accepted or rejected'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class AccountRequestList(APIView):
    def get(self, request):
        opening_requests = AccountOpeningRequest.objects.filter(
            status="PENDING"
        )

        serializer = AccountOpeningRequestSerializer(
            opening_requests,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class AccountDetailView(APIView):

    def get(self, request):
        account_number = request.query_params.get('number')
        account = BankAccount.objects.select_related('customer').get(
            account_number=account_number
        )

        serializer = CustomerAccountSerializer(account)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class BankAccountDepositView(APIView):

    def patch(self, request):
        try:
            account_number = request.query_params.get('account_number')
            amount = int (request.query_params.get('amount'))
            saved_account = make_deposit(
                account_number=account_number,
                amount=amount
            )

            serializer = NewAccountDetailsSerializer(saved_account)

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                data={
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class BankAccountWithdrawView(APIView):

    def patch(self, request):
        try:
            account_number = request.query_params.get('account_number')
            amount = int (request.query_params.get('amount'))

            saved_account = make_withdraw(
                account_number=account_number,
                amount=amount
            )

            serializer = NewAccountDetailsSerializer(saved_account)

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        except ValueError as e:

            return Response(
                data={
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except InsufficientBalanceException as e:
            return Response(
                data={
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )