# Generated by Django 4.2.6 on 2023-12-13 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0018_completed_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='is_what',
            field=models.CharField(choices=[('PREPARING', 'PREPARING'), ('OUT FOR DELIVERY', 'OUT FOR DELIVERY')], default='', null=True),
        ),
    ]
