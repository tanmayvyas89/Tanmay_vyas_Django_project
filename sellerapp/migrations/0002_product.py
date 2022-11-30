# Generated by Django 4.1.1 on 2022-11-05 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('des', models.TextField()),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField(default=0)),
                ('discount', models.IntegerField()),
                ('pic', models.FileField(default='avatar.png', upload_to='products')),
                ('discountedprice', models.FloatField(blank=True, null=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerapp.seller')),
            ],
        ),
    ]
