from urllib.parse import urlencode

import requests
from django.conf import settings


class FinanceApi:
    def __init__(self):
        self.access_token = None

    def set_access_token(self, access_token: str):
        self.access_token = access_token

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}'
        }

    def _get_model_list(self, url, **kwargs):
        query = urlencode(kwargs)
        response = requests.get(
            f"{url}?{query}",
            headers=self.get_headers(),
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"HTTP {response.status_code}: {response.text}")

    def get_records(self, **kwargs):
        return self._get_model_list(settings.FINANCE_RECORD_ENDPOINT, **kwargs)

    def get_categories(self, **kwargs):
        return self._get_model_list(settings.FINANCE_CATEGORY_ENDPOINT, **kwargs)

    def get_contracts(self, **kwargs):
        return self._get_model_list(settings.FINANCE_CONTRACT_ENDPOINT, **kwargs)

    def create_records(self, records):
        response = requests.post(
            settings.FINANCE_RECORD_ENDPOINT,
            headers=self.get_headers(),
            json=records,
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(f"HTTP {response.status_code}: {response.text}")
