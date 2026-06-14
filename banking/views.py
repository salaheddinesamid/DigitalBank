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
from .models import AccountOpeningRequest, BankAccount


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
                    'error' : 'This opening request may have already been accepted or rejected'
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