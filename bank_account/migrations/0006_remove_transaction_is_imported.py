# Generated by Django 5.1.2 on 2024-10-27 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0005_transaction_is_ready'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='is_imported',
        ),
    ]
