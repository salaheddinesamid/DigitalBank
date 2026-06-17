from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ViewSet

# Import services
from ..services.deposit_service import make_deposit
from ..services.withdraw_service import make_withdraw
from ..services.transfer_service import make_internal_transfer
from ..exceptions.insufficent_balance_exception import InsufficientBalanceException

# Import serializers
from ..serializers.account_opening_serializer import NewAccountDetailsSerializer
from ..serializers.transaction_serializer import TransactionSerializer, TransactionDetailSerializer
from ..serializers.transfer_serializer import TransferSerializer
from rest_framework.response import Response
from rest_framework import status

from DigitalBank.security.permissions import IsCustomer


@method_decorator(csrf_exempt, name='dispatch')
class AccountTransactionViewSet(ViewSet):
    @action(detail=False, methods=["post"], permission_classes=[IsCustomer], throttle_classes=[UserRateThrottle])
    def deposit(self, request):
        try:
            data = TransactionSerializer(
                data=request.data
            )
            if data.is_valid():
                saved_account = make_deposit(
                    data.validated_data,
                    user=request.user
                )

                serializer = NewAccountDetailsSerializer(saved_account)

                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(status=status.HTTP_502_BAD_GATEWAY)

        except InsufficientBalanceException as e:
            return Response(
                data={
                    "error" : str(e)
                },
                status=status.HTTP_409_CONFLICT
            )
        except ValueError as e:
            return Response(
                data={
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"], permission_classes = [IsCustomer])
    def withdraw(self, request):
        try:
            data = TransactionSerializer(
                data=request.data
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

    @action(detail=False, methods=["post"], permission_classes = [IsCustomer])
    def transfer(self, request):

        try:
            serializer = TransferSerializer(
                data=request.data
            )

            serializer.is_valid(raise_exception=True)

            if serializer.validated_data["type"] == "INTERNAL":
                transfer = make_internal_transfer(
                    serializer.validated_data
                )

                response_serializer = TransactionDetailSerializer(
                    transfer
                )

                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED
                )

            return Response(
                {"error": "Unsupported transfer type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except InsufficientBalanceException as e:
            return Response(
                data={
                    "error" : str(e)
                },
                status=status.HTTP_409_CONFLICT
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
