from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from .models import ExchangeRate, Currency
from django.utils import timezone
from datetime import datetime
import json


class ExchangeRateTests(APITestCase):

    def test_valid_request(self):
        Currency.objects.create(code="EUR")
        Currency.objects.create(code="USD")

        naive_timestamp = datetime.now()
        timestamp = timezone.make_aware(naive_timestamp, timezone.get_current_timezone())
        ExchangeRate.objects.create(currency_pair="EURUSD", timestamp=timestamp, exchange_rate=0.85)

        response = self.client.get('/currency/EUR/USD/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_with_no_data(self):
        Currency.objects.create(code="EUR")
        Currency.objects.create(code="USD")

        response = self.client.get('/currency/EUR/USD/')
        response_data = json.loads(response.content)
        self.assertEqual(response_data['response'], "No data for EURUSD pair!")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_with_invalid_currecies(self):
        Currency.objects.create(code="EUR")

        response = self.client.get('/currency/EUR/USD/')
        response_data = json.loads(response.content)
        self.assertEqual(response_data['response'], "Currency USD does not exist!")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_with_same_currecies(self):
        Currency.objects.create(code="EUR")

        response = self.client.get('/currency/EUR/EUR/')
        response_data = json.loads(response.content)
        self.assertEqual(response_data['response'], "Comparing same currency is not supported!")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
