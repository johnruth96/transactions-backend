# Generated by Django 5.1.2 on 2024-10-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0002_transaction_is_counter_to_transaction_is_ignored'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_imported',
            field=models.BooleanField(default=False),
        ),
    ]