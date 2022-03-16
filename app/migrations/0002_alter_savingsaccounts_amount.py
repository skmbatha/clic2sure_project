# Generated by Django 4.0.3 on 2022-03-15 18:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savingsaccounts',
            name='amount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(50.0)]),
        ),
    ]
