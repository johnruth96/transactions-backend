import csv
import logging
from datetime import datetime
from io import StringIO
from pprint import pformat
from urllib.request import urlopen

from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from bank_account.api import FinanceApi
from bank_account.models import Transaction, RecordProxy, Account
from bank_account.serializers import TransactionSerializer, RecordProxySerializer

logger = logging.getLogger()


def import_remote_records(data):
    with transaction.atomic():
        for record_dict in data:
            logger.debug(f"")

            params = dict(
                date=datetime.strptime(record_dict["date"], '%Y-%m-%d'),
                subject=record_dict["subject"],
                amount=record_dict["amount"],
                account=record_dict["account"],
                category=record_dict["category"],
                contract=record_dict["contract"],
            )

            record = RecordProxy.objects.filter(remote_id=record_dict["id"])
            if record.exists():
                logger.debug(f"Update RecordProxy from remote: {pformat(record_dict)}")
                record.update(**params)
            else:
                logger.debug(f"Create RecordProxy from remote: {pformat(record_dict)}")
                RecordProxy.objects.create(
                    remote_id=record_dict["id"],
                    **params
                )


def import_csv(reader: csv.reader):
    reading_payload = False
    contains_saldo = False

    iban = None
    name = None

    transactions = []
    for row in reader:
        if not row:
            continue

        if row[0] == "IBAN":
            iban = row[1].replace(" ", "").strip()

        if row[0] == "Kontoname":
            name = row[1]

        if row[0] == "Saldo":
            contains_saldo = True
            logger.debug("File contains 'Saldo'")

        if row[0] == "Buchung":
            reading_payload = True
            continue

        if reading_payload:
            amount_str = row[7] if contains_saldo else row[5]
            currency = row[8] if contains_saldo else row[6]

            transactions.append(dict(
                booking_date=datetime.strptime(row[0], "%d.%m.%Y"),
                value_date=datetime.strptime(row[1], "%d.%m.%Y"),
                creditor=row[2],
                transaction_type=row[3],
                purpose=row[4],
                amount=float(amount_str.replace(".", "").replace(",", ".")),
                currency=currency,
            ))

    with transaction.atomic():
        account, _ = Account.objects.get_or_create(
            iban=iban,
            name=name,
        )

        num_created = 0
        for transaction_dict in transactions:
            _, created = Transaction.objects.get_or_create(
                account=account,
                **transaction_dict,
            )

            if created:
                num_created += 1

        logger.debug(f"Done. Added {num_created}/{len(transactions)} transactions")


class CategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        api = FinanceApi()
        api.set_access_token(request.auth)
        return Response(api.get_categories())


class ContractListView(APIView):
    def get(self, request, *args, **kwargs):
        api = FinanceApi()
        api.set_access_token(request.auth)
        return Response(api.get_contracts())


class RecordProxyViewSet(viewsets.ModelViewSet):
    queryset = RecordProxy.objects.all()
    serializer_class = RecordProxySerializer

    @action(methods=["POST"], detail=False)
    def fetch(self, request, pk=None):
        api = FinanceApi()
        api.set_access_token(request.auth)

        # Import
        # TODO: Parameterize date_start
        records = api.get_records(date_start="2024-09-01")
        logger.debug(f"Successfully fetched {len(records)} records")

        import_remote_records(records)

        # Deletions
        records = api.get_records(date_start="2024-08-01")
        remote_ids = set(record['id'] for record in records)
        local_ids = set(RecordProxy.objects.values_list("remote_id", flat=True))
        maybe_deleted = local_ids.difference(remote_ids)
        logger.debug(f"{len(maybe_deleted)} RecordProxy objects are possibly deleted.")

        for pk in maybe_deleted:
            if pk is None:
                continue

            record = RecordProxy.objects.get(remote_id=pk)
            logger.debug(f"Local Record '{record.subject}' ({record.date}) not found on Remote. Delete?")
            # choice = input("[n] ")
            # if choice == "y":
            #    record.delete()

        return Response(status=204)

    @action(methods=["POST"], detail=False)
    def publish(self, request, pk=None):
        api = FinanceApi()
        api.set_access_token(request.auth)

        records = RecordProxy.objects.filter(pk__in=request.data)

        if records.filter(remote_id__isnull=False).exists():
            raise APIException("Cannot publish records from remote.")

        records_list = list(records)
        records_data = []
        for record in records_list:
            record_data = dict(
                subject=record.subject,
                account=record.account,
                category=record.category,
                contract=record.contract,
                date=record.date.strftime('%d.%m.%Y'),
                amount=float(record.amount),
            )
            records_data.append(record_data)

        remote_records = api.create_records(records_data)

        for proxy, remote_data in zip(records_list, remote_records):
            proxy.remote_id = remote_data["id"]
            proxy.save()

        return Response(status=204)

    @action(methods=["DELETE"], detail=False)
    def bulk_delete(self, request, pk=None):
        records = RecordProxy.objects.filter(pk__in=request.data)

        if records.filter(remote_id__isnull=False).exists():
            raise APIException("Cannot delete records from remote.")

        records.delete()

        return Response(status=204)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(methods=["POST"], detail=True)
    def hide(self, request, pk=None):
        t = Transaction.objects.get(pk=pk)

        if t.is_imported:
            raise APIException("Transaction is imported.")

        t.is_ignored = True
        t.save()

        return Response(data=TransactionSerializer(t).data)

    @action(methods=["POST"], detail=True)
    def show(self, request, pk=None):
        t = Transaction.objects.get(pk=pk)

        if not t.is_ignored:
            raise APIException("Transaction is not ignored.")

        t.is_ignored = False
        t.save()

        return Response(data=TransactionSerializer(t).data)

    @action(methods=["POST"], detail=True)
    def bookmark(self, request, pk=None):
        t = Transaction.objects.get(pk=pk)
        t.is_highlighted = True
        t.save()
        return Response(data=TransactionSerializer(t).data)

    @action(methods=["POST"], detail=True)
    def unbookmark(self, request, pk=None):
        t = Transaction.objects.get(pk=pk)
        t.is_highlighted = False
        t.save()
        return Response(data=TransactionSerializer(t).data)

    @action(methods=["POST"], detail=False)
    def counter_booking(self, request, pk=None):
        if len(request.data) != 2:
            raise ValidationError()

        pk_a = request.data[0]
        pk_b = request.data[1]

        tr_a = Transaction.objects.get(pk=pk_a)
        tr_b = Transaction.objects.get(pk=pk_b)

        if tr_a.account != tr_b.account:
            raise ValidationError()

        tr_a.is_counter_to = tr_b
        tr_b.is_counter_to = tr_a

        tr_a.save()
        tr_b.save()

        return Response(status=200)

    @action(methods=["POST"], detail=True)
    def records(self, request, pk=None):
        t = Transaction.objects.get(pk=pk)
        records = RecordProxy.objects.filter(pk__in=request.data)
        t.records.set(records)

        return Response(data=TransactionSerializer(t).data)

    @action(methods=["POST"], detail=False, url_path="import")
    def import_csv(self, request, pk=None):
        logger.debug(f"Process files: {request.data}")

        # Except: CSV file with delimiter ";"
        if not isinstance(request.data, list):
            raise ValidationError()

        with transaction.atomic():
            for data_uri in request.data:
                with urlopen(data_uri) as response:
                    data = response.read()

                f = StringIO(data.decode("iso-8859-1"))
                reader = csv.reader(f, delimiter=";")
                import_csv(reader)

        return Response(status=204)
