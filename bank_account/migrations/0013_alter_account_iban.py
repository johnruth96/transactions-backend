# Generated by Django 5.1.2 on 2024-12-30 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_account', '0012_recordproxy_account_recordproxy_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='iban',
            field=models.CharField(max_length=22),
        ),
    ]
