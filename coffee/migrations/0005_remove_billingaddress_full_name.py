# Generated by Django 4.2.6 on 2023-11-09 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0004_billingaddress_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='full_name',
        ),
    ]