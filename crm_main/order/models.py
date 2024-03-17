from django.db import models
from django.contrib.auth.models import User
from client.models import Client

# Create your models here.

class Order(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='orders', on_delete=models.CASCADE)  # Added field
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=PENDING)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipment_company = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    shiping_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number}"
