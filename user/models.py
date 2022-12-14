from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import Product


# Create your models here.


class User(AbstractUser):
    MALE_STATUS = 1
    FEMALE_STATUS = 2
    OTHER_STATUS = 3
    GENDER_CHOICES = (
        (MALE_STATUS, 'Male'),
        (FEMALE_STATUS, 'Female'),
        (OTHER_STATUS, 'Other')
    )
    phone = models.CharField(default='', max_length=10)
    address = models.CharField(default='', max_length=255)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    email_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
