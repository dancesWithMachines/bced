from .serializers import CurrencySerializer, ExchangeRateSerializer
from rest_framework.response import Response
from .constants import SUPPORTED_CURRENCIES
from .models import Currency, ExchangeRate
from rest_framework.views import APIView
from rest_framework import status


class CurrencyListApiView(APIView):

    def get(self, request, *args, **kwargs):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrencyRatesApiView(APIView):

    def get(self, request, base_currency_code, currency_code, *args, **kwargs):
        if base_currency_code == currency_code:
            return Response(
                {"response": f"Comparing same currency is not supported!"}, status=status.HTTP_400_BAD_REQUEST
            )

        for code in base_currency_code, currency_code:
            try:
                Currency.objects.get(code=code)
            except Currency.DoesNotExist:
                return Response({"response": f"Currency {code} does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            if code not in SUPPORTED_CURRENCIES:
                return Response(
                    {"response": f"Currency {code} is not supported yet!"}, status=status.HTTP_400_BAD_REQUEST
                )

        try:
            exchange_rate = exchange_rate = ExchangeRate.objects.filter(
                currency_pair=f'{base_currency_code}{currency_code}'
            ).order_by('-timestamp').first()
        except ExchangeRate.DoesNotExist:
            return Response(
                {"response": f"Currency pair {base_currency_code}{currency_code} does not exist!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ExchangeRateSerializer(exchange_rate)
        if not serializer.data["exchange_rate"]:
            return Response(
                {"response": f"No data for {base_currency_code}{currency_code} pair!"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {"exchange_rate": serializer.data["exchange_rate"]}

        return Response(data, status=status.HTTP_200_OK)
