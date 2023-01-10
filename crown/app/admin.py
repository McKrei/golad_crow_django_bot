from django.contrib import admin

from app.models import *



admin.site.register(Currency)
admin.site.register(Country)
admin.site.register(CurrencyPairs)
admin.site.register(HistoryPrice)

