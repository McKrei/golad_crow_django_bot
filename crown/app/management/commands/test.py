import asyncio
from django.core.management.base import BaseCommand

from parser.main import GetDataGoldCrown
from app.models import *
from user.models import *


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        for country in countries:
            pairs = list(CurrencyPairs.objects.filter(
                country_receive=country).values_list(
                'currency_receive__name',
                'price',
                ))
            print(country.name)
            print(pairs)
