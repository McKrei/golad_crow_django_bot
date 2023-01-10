import time
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from app.models import HistoryPrice
from user.models import UserWaiting, UserPairs
from bot.misc.mes import send_messages


def find_second_hours(send_hour=None):
    now = datetime.now()
    seconds = 0
    if not send_hour:
        send_hour = (now + timedelta(hours=1)).hour

    if now.hour < send_hour:
        seconds = (now.replace(
            hour=send_hour, minute=0, second=0
            ) - now).seconds
    else:
        tomorrow = now + timedelta(days=1)
        seconds = (tomorrow.replace(
            hour=send_hour, minute=0, second=0
            ) - tomorrow).seconds
    return seconds, now.hour


def checking_price_every_hour_and_send_mes_every_day():
    hour = 13
    history_price = HistoryPrice()
    user_wait = UserWaiting()
    user_pairs = UserPairs()
    while True:
        try:
            all_price = history_price.update_data()
            reports = user_wait.create_report_update_user_waiting(all_price)
            if reports:
                async_to_sync(send_messages)(reports)
            seconds, now_hour = find_second_hours()
            if now_hour == hour:
                reports = user_pairs.create_report_update_user_pairs()
                if reports:
                    async_to_sync(send_messages)(reports)
        except Exception as e:
            print(e)

        time.sleep(seconds)
