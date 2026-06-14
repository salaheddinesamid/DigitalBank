"""
URL configuration for DigitalBank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import AccountCreationView, AccountRequestList, AccountOpeningRequestUpdate, AccountDetailView

urlpatterns = [
    path('customer_management/new', AccountCreationView.as_view()),
    path('customer_management/get', AccountDetailView.as_view()),
    path('customer_management/requests/get_all', AccountRequestList.as_view()),
    path('customer_management/requests/update/<int:pk>', AccountOpeningRequestUpdate.as_view())
]
