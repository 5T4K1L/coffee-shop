# Generated by Django 4.2.6 on 2023-11-11 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0008_billingaddress_is_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='is_complete',
            field=models.CharField(choices=[('NO', 'NO'), ('YES', 'YES')], default='', null=True),
        ),
    ]
