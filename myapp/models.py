from django.db import models
from sellerapp import *
from sellerapp.models import Product

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    Email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name


class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    


