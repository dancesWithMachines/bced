from .models import Currency, ExchangeRate
from rest_framework import serializers


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ["code"]


class ExchangeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeRate
        fields = ["base_currency", "second_currency", "timestamp", "exchange_rate"]
