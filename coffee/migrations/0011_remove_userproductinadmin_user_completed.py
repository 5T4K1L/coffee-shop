# Generated by Django 4.2.6 on 2023-11-11 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coffee', '0010_userproductinadmin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userproductinadmin',
            name='user',
        ),
        migrations.CreateModel(
            name='Completed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coffee.products')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]