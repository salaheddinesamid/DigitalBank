from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    SUSPENDED = "SUSPENDED", "Suspended"
    PENDING = "PENDING", "Pending Verification"


class RoleNames(models.TextChoices):
    CUSTOMER = "CUSTOMER", "Customer",
    BANKER = "BANKER", "Banker",
    ADMIN = "ADMIN", "Admin"


class Role(models.Model):
    role_name = models.CharField(
        max_length=200,
        choices=RoleNames.choices
    )


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    roles=models.ManyToManyField(
        Role,
        related_name='users',
        blank=True
    )


class Customer(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    CIN = models.CharField(max_length=200, unique=True, null=False, default=None)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        unique=True
    )
