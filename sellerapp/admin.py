from django.contrib import admin
from . models import *

# Register your models here.
@admin.register(Seller)
class UserAdmin(admin.ModelAdmin):
    list_display=['id', 'first_name','Email','password']

@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display=['id','product_name','product_description','price','quantity','discounted_price','seller','image']


