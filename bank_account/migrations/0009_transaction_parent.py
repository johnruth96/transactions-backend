# Generated by Django 5.1.2 on 2024-10-31 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0008_rename_is_marked_transaction_is_highlighted'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='bank_account.transaction'),
        ),
    ]