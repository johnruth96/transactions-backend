from django.db import models


class Account(models.Model):
    iban = models.CharField(max_length=22)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.iban


class RecordProxy(models.Model):
    """
    Model represents a Record object of the 'finance' app.
    """
    remote_id = models.IntegerField(unique=True, null=True)
    date = models.DateTimeField()
    subject = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.IntegerField(null=True)
    category = models.IntegerField(null=True)
    contract = models.IntegerField(null=True)

    class Meta:
        ordering = ('date', 'subject')


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    booking_date = models.DateTimeField()
    value_date = models.DateTimeField()
    creditor = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    currency = models.CharField(max_length=3)
    transaction_type = models.TextField()
    purpose = models.TextField()

    # Meta data
    is_ignored = models.BooleanField(default=False)
    is_counter_to = models.ForeignKey('bank_account.Transaction', on_delete=models.SET_NULL, null=True)
    is_highlighted = models.BooleanField(default=False)

    records = models.ManyToManyField(RecordProxy, related_name='transactions')

    @property
    def is_new(self):
        return not self.records.exists() and not self.is_ignored

    @property
    def is_in_progress(self):
        return self.records.filter(remote_id__isnull=True).exists() and not self.is_ignored

    @property
    def is_imported(self):
        imported_count = self.records.filter(remote_id__isnull=False).count()
        return self.records.exists() and self.records.count() == imported_count and not self.is_ignored

    class Meta:
        ordering = ('booking_date',)
