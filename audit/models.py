from django.db import models
from customer_management.models import Customer


# Create your models here.

class AuditLog(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )

    action = models.CharField(
        max_length=100
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
