from .views import CurrencyListApiView, CurrencyRatesApiView
from django.urls import path

urlpatterns = [
    path("", CurrencyListApiView.as_view()),
    path("<str:base_currency_code>/<str:currency_code>/", CurrencyRatesApiView.as_view())
]
