from .serializers import CurrencySerializer, ExchangeRateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status, generics
from .constants import SUPPORTED_CURRENCIES
from .models import Currency, ExchangeRate
from rest_framework.views import APIView


class CurrencyListApiView(APIView):

    def get(self, request, *args, **kwargs):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrencyRatesApiView(generics.ListCreateAPIView):

    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    ordering_fields = ['timestamp', 'exchange_rate']
    filterset_fields = ['base_currency', 'second_currency', 'timestamp', 'exchange_rate']
