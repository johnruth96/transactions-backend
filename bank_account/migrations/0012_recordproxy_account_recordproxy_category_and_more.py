# Generated by Django 5.1.2 on 2024-11-15 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0011_alter_recordproxy_id_alter_transaction_records'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordproxy',
            name='account',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recordproxy',
            name='category',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recordproxy',
            name='contract',
            field=models.IntegerField(null=True),
        ),
    ]
