# Generated by Django 4.0.3 on 2022-03-15 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_transactions_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='account_id',
            field=models.IntegerField(default=-1),
        ),
    ]
