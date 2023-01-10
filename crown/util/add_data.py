import re

from app.models import CurrencyPairs
from user.models import UserWaiting
from asgiref.sync import sync_to_async


async def validated_price(mes, now_price):
    num = re.findall(r'\d+.\d+', mes)
    if not num:
        num = re.findall(r'\d+', mes)
        if not num:
            return 0
    num = float(num[0])
    if mes.count('%'):
        num = round(now_price * (num / 100), 2)
        if not mes.count('+') and not mes.count('-'):
            return num + now_price
    if mes.count('+'):
        return num + now_price
    if mes.count('-'):
        return now_price - num
    return round(num, 2)


async def add_user_waiting(user_id, pairs_id, message):
    cp = CurrencyPairs()
    now_price = await sync_to_async(cp.get_price)(pairs_id)
    price = await validated_price(message, now_price)
    if not price:
        return False, 'Не понял какую цену хотите'
    is_more = price > now_price
    uw = UserWaiting()
    result = await sync_to_async(uw.add)(user_id, pairs_id, price, is_more)
    return True, result
