# Generated by Django 5.1.2 on 2024-10-27 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0004_recordproxy_alter_transaction_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_ready',
            field=models.BooleanField(default=False),
        ),
    ]
