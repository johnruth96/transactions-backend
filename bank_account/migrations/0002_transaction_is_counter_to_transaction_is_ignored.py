# Generated by Django 5.1.2 on 2024-10-25 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_counter_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank_account.transaction'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_ignored',
            field=models.BooleanField(default=False),
        ),
    ]
