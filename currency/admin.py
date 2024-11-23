from django_apscheduler.models import DjangoJob, DjangoJobExecution
from django.contrib.auth.models import User, Group
from django.contrib import admin
from .models import ExchangeRate

admin.site.unregister(DjangoJob)
admin.site.unregister(DjangoJobExecution)
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("currency_pair", "timestamp", "exchange_rate")
    list_filter = ("currency_pair",)
    ordering = ("currency_pair", "timestamp")
    search_fields = ("currency_pair",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by("currency_pair", "timestamp")
