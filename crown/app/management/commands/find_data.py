import asyncio
from django.core.management.base import BaseCommand

from parser.main import GetDataGoldCrown
from app.models import HistoryPrice
from user.models import User


class Command(BaseCommand):
    help = 'Заходим на сайт золотой короны и собираем данные по странам, валютам и возможным парам'\
           'Заполняем этими данными смежные таблицами для корректной дальнейшей работы'\
            'Устанавливаем админа, для отправки дампа и ошибок'

    def handle(self, *args, **kwargs):
        # Добавляем админа
        id = 415598571
        admin = User(id=id, is_admin=True)
        admin.save()

        his_price = HistoryPrice()
        his_price.update_data()
