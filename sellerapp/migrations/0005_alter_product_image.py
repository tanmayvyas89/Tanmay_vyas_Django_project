# Generated by Django 4.1.1 on 2022-11-09 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0004_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(default='avatar.png', upload_to='manageproduct'),
        ),
    ]
