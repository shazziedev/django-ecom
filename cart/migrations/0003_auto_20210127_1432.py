# Generated by Django 3.1.4 on 2021-01-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20210127_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='orderitems',
        ),
        migrations.AddField(
            model_name='order',
            name='orderitems',
            field=models.ManyToManyField(related_name='orderitems', to='cart.Cart'),
        ),
    ]
