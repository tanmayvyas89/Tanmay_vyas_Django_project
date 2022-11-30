from django.db import models
from .import *

# Create your models here.
class Seller(models.Model):
    first_name = models.CharField(max_length=30)
    Email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)

def __str__(self):
        return self.first_name

class Product(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)  # Foreignkey
    product_name = models.CharField(max_length=50)
    product_description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    discount = models.IntegerField()
    image = models.FileField(upload_to='manageproduct',default='avatar.png')    
    discounted_price = models.FloatField(blank=True,null=True)
    first_name = models.CharField(max_length=50)

    
    def __str__(self):
        return self.first_name



