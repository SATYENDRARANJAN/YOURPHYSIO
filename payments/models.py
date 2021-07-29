from django.db import models

# Create your models here.
from django.db import models

from users.models import Patient


class Transaction(models.Model):
    PAYMENT_STATUS = (('SUCCESS','SUCCESS'),('FAILED','FAILED'),('PENDING','PENDING'))
    payment_order_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=PAYMENT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

