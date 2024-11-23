from .models import Currency, ExchangeRate
from rest_framework import serializers


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ["code"]


class ExchangeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeRate
        fields = ["currency_pair", "timestamp", "exchange_rate"]
