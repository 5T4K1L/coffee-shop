# Generated by Django 4.2.6 on 2023-12-14 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0020_alter_billingaddress_is_what'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='is_what',
            field=models.CharField(choices=[('ORDER RECEIVED BY SELLER', 'ORDER RECEIVED BY SELLER'), ('PREPARING', 'PREPARING'), ('OUT FOR DELIVERY', 'OUT FOR DELIVERY')], default='ORDER RECEIVED BY SELLER', null=True),
        ),
    ]
