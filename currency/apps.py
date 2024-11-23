from django.apps import AppConfig
import logging

logger = logging.getLogger('currency')


class CurrencyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'currency'

    def ready(self):
        from .tasks import start, fetch_exchange_rates
        start()
