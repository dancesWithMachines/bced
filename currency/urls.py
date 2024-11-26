from .views import CurrencyListApiView, CurrencyRatesApiView
from django.urls import path

urlpatterns = [path("", CurrencyListApiView.as_view()), path("all/", CurrencyRatesApiView.as_view())]
