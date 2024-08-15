# Generated by Django 5.0.6 on 2024-07-25 03:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='full_name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Full name must contain only letters', regex="^[A-Za-z\\s'-]+$")]),
        ),
    ]
