
# from multiprocessing import Process
from threading import Thread

from django.core.management.base import BaseCommand
from util.waiting import checking_price_every_hour_and_send_mes_every_day
from bot.main import runbot


class Command(BaseCommand):
    help = 'Запускаем 2-а процесса'\
           '1 - запускаем бот'\
           '2 - запускаем систематическую проверку цен'


    def handle(self, *args, **kwargs):
        thread = Thread(target=checking_price_every_hour_and_send_mes_every_day)
        thread.start()
        runbot()
