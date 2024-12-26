from rest_framework import serializers

from bank_account.models import Transaction, RecordProxy


class RecordProxySerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(many=True, queryset=Transaction.objects.all())

    class Meta:
        model = RecordProxy
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()
    records = serializers.PrimaryKeyRelatedField(many=True, queryset=RecordProxy.objects.all())

    class Meta:
        model = Transaction
        fields = '__all__'
