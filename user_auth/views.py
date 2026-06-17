from django.shortcuts import render
from user_auth.serializers.CustomTokenSerializer import CustomTokenSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

# Create your views here.

class AuthenticationView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
