# Generated by Django 5.1.2 on 2024-11-10 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0009_transaction_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='is_ready',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='parent',
        ),
        migrations.AddField(
            model_name='recordproxy',
            name='remote_id',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
