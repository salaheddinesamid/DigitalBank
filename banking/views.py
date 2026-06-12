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
from .serializers.account_opening_serializer import AccountOpeningRequestSerializer
from .services.new_account_service import create_new_account


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