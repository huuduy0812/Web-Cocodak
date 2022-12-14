from django.db import models
from user.models import User
from cart.models import Cart
from product.models import Product
# Create your models here.


class Order(models.Model):
    name = models.CharField(default='', max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    shipping_address = models.CharField(max_length=255, default='')
    PROCESSING_STATUS = 1
    Delivery_in_processing_STATUS = 2
    COMPLETED_STATUS = 3
    CANCELED_STATUS = 4
    STATUS_CHOICES = (
        (PROCESSING_STATUS, 'Processing'),
        (Delivery_in_processing_STATUS, 'Delivery in processing'),
        (COMPLETED_STATUS, 'Completed'),
        (CANCELED_STATUS, 'Canceled'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=PROCESSING_STATUS)
    ship = models.FloatField(default=1.9)
    payment = models.BooleanField(default=False)
    phone = models.CharField(max_length=255, default='')
    total = models.FloatField(default=0, blank=True, null=True)
    total_all = models.FloatField(default=0, blank=True, null=True)


class Orderitem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(default=0, blank=True, null=True)
