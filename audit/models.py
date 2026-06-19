from django.db import models
from customer_management.models import User


# Create your models here.

class AuditLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    action = models.CharField(
        max_length=100
    )

    ip_address = models.CharField(
        max_length=230,
        default=None,
        null=True
    )

    entity = models.CharField(
        max_length=100
    )

    entity_id = models.IntegerField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    details = models.JSONField(
        null=True,
        blank=True
    )
