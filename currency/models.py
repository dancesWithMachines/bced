from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.code

    class Meta:
        ordering = ['code']


class ExchangeRate(models.Model):
    currency_pair = models.CharField(max_length=6)
    timestamp = models.DateTimeField()
    exchange_rate = models.FloatField()

    def __str__(self) -> str:
        return self.currency_pair

    class Meta:
        ordering = ['timestamp']
