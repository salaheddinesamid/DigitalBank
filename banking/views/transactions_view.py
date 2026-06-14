from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from ..services.deposit_service import make_deposit
from ..services.withdraw_service import make_withdraw
from ..exceptions.insufficent_balance_exception import InsufficientBalanceException
from ..serializers.account_opening_serializer import NewAccountDetailsSerializer
from ..serializers.transaction_serializer import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status


@method_decorator(csrf_exempt, name='dispatch')
class AccountTransactionViewSet(ViewSet):
    @action(detail=False, methods=["patch"])
    def deposit(self, request):
        try:

            data = TransactionSerializer(
                data=request.data
            )
            if data.is_valid():
                saved_account = make_deposit(
                    data.validated_data
                )

                serializer = NewAccountDetailsSerializer(saved_account)

                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(status=status.HTTP_502_BAD_GATEWAY)
        except ValueError as e:
            return Response(
                data={
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["patch"])
    def withdraw(self, request):
        try:
            data = TransactionSerializer(
                data=request    .data
            )

            if data.is_valid():
                saved_account = make_withdraw(
                    validate_data=data.validated_data
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
