# Generated by Django 4.2.6 on 2023-11-09 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0003_billingaddress_usersordernotif'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='total_price',
            field=models.CharField(default='', max_length=1000, null=True),
        ),
    ]
