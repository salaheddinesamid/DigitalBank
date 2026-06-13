from django.shortcuts import render
from rest_framework.views import APIView
from .serializers.new_account_serializer import NewAccountSerializer


# Create your views here.

class CreateAccountView(APIView):
    def post(self, request):

        # Extract the data from HTTP request
        validated_data = NewAccountSerializer(
            data=request.data
        )

        # Process the account creation request
