from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.code

    class Meta:
        ordering = ['code']


class ExchangeRate(models.Model):
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="base_currency")
    second_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="second_currency")
    timestamp = models.DateTimeField()
    exchange_rate = models.FloatField()

    def __str__(self) -> str:
        return f'{self.base_currency}{self.second_currency}'

    class Meta:
        ordering = ['timestamp']
