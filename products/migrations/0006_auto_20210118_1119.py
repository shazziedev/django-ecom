# Generated by Django 3.1.4 on 2021-01-18 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_moreimgdetails_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='more',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='more', to='products.moreimgdetails'),
        ),
    ]
