from django.contrib import admin

from bank_account.models import Account, Transaction

admin.register(Account)
admin.register(Transaction)
