# Generated by Django 4.1.1 on 2022-11-05 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0002_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discountedprice',
            new_name='discounted_price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='pic',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='des',
            new_name='product_description',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='product_name',
        ),
    ]
