from .serializers import CurrencySerializer, ExchangeRateSerializer
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Currency, ExchangeRate
from .constants import SUPPORTED_CURRENCIES
from itertools import permutations
from rest_framework import status
from django.utils import timezone
from datetime import datetime
import yfinance as yf
import requests
import logging
import json

logger = logging.getLogger('currency')


# I know this is overkill, new (non-crypto) currencies do not grow overnight, but why not automate it
def fetch_currency_codes():
    logger.info("Fetching currency codes!")
    response = requests.get("https://openexchangerates.org/api/currencies.json")

    if response.status_code == status.HTTP_200_OK:
        response_data = response.json()
        currency_codes = [{"code": code} for code in response_data.keys()]

        for data in currency_codes:

            if Currency.objects.filter(code=data["code"]).exists():
                continue

            serializer = CurrencySerializer(data=data)

            if serializer.is_valid():
                serializer.save()
    else:
        logger.error("Failed to fetch currency codes!")


def fetch_exchange_rates():
    logger.info("Fetching exchange rates!")

    # Let's just do 4 popular ones, this would take forever
    # currency_permutations = permutations(Currency.objects.values_list('code', flat=True), 2)
    currency_permutations = perm = permutations(SUPPORTED_CURRENCIES, 2)

    for pair in currency_permutations:
        currency_pair = f"{pair[0]}{pair[1]}"
        exchange_data = yf.download(currency_pair + "=X", period="1d", interval="1h", progress=False).to_json()
        exchange_data = json.loads(exchange_data)
        # Let's just fetch open for this task
        exchange_data_for_open = exchange_data[f"('Open', '{currency_pair}=X')"]

        for key, value in exchange_data_for_open.items():
            timestamp = datetime.fromtimestamp(int(key) / 1000)
            timestamp = timezone.make_aware(timestamp, timezone.get_default_timezone())

            if ExchangeRate.objects.filter(timestamp=timestamp, currency_pair=currency_pair).exists():
                continue

            data = {"currency_pair": currency_pair, "timestamp": timestamp, "exchange_rate": value}

            seralizer = ExchangeRateSerializer(data=data)

            if seralizer.is_valid():
                seralizer.save()

    logger.info("Fetching exchange rates finished!")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_currency_codes, 'interval', days=1, next_run_time=datetime.now())
    scheduler.add_job(fetch_exchange_rates, 'interval', hours=1, next_run_time=datetime.now())
    scheduler.start()

    start._scheduler_started = True
