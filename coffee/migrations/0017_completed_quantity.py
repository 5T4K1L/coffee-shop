# Generated by Django 4.2.6 on 2023-11-12 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0016_completed_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='completed',
            name='quantity',
            field=models.CharField(default='', max_length=1000, null=True),
        ),
    ]
