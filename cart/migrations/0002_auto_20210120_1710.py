# Generated by Django 3.1.4 on 2021-01-20 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderId',
            field=models.CharField(default=None, max_length=120),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_fee',
            field=models.DecimalField(decimal_places=2, default=5.99, max_digits=100),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Not Yet Shipped', 'Not Yet Shipped'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Refunded', 'Refunded')], default='Not Yet Shipped', max_length=120),
        ),
    ]
