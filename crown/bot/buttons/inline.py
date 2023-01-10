from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async

from app.models import *
from user.models import *



async def get_all_buttons_my_currency(user_id) -> InlineKeyboardMarkup:
    uw = UserWaiting()
    up = UserPairs()


    lst_pairs = await sync_to_async(up.get)(user_id)

    if not lst_pairs:
        return [{'text' : 'Вы не выбрали себе валюту'}]

    lst_waiting_pairs = await sync_to_async(uw.get)(user_id)


    dct_waiting_pairs = {}
    for id, pairs_id, price, is_more in lst_waiting_pairs:
        if dct_waiting_pairs.get(pairs_id):
            dct_waiting_pairs[pairs_id].append((id, price, is_more))
        else:
            dct_waiting_pairs[pairs_id] = [(id, price, is_more)]

    result_inlines = []
    for pairs_id, currency, country, price, is_report in lst_pairs:
        report = 'вкл.' if is_report else 'выкл.'
        buttons = [
            InlineKeyboardButton(f'Отчет {report}',
                callback_data=f'fp_{pairs_id}'),
            InlineKeyboardButton('Удалить',
                callback_data=f'DP_{pairs_id}'),
            InlineKeyboardButton('Добавить',
                callback_data=f'ad_{pairs_id}'),
            ]
        inline = InlineKeyboardMarkup(row_width=3).add(*buttons)

        data = dct_waiting_pairs.get(pairs_id)
        if data:
            for uw_id, user_price, is_more in data:
                big_little = 'больше' if is_more else 'меньше'
                inline.row(
                    InlineKeyboardButton(
                        f'Жду {big_little} {float(user_price)} руб. /удалить',
                        callback_data=f'DUW_{uw_id}'),
                )

        result_inlines.append(
            {
                'text' : f'{country} {currency} {float(price)} руб.',
                'reply_markup' : inline
            }
        )

    return result_inlines


async def get_all_buttons_currency() -> InlineKeyboardMarkup:
    cur_pairs = CurrencyPairs()
    pairs_country = await sync_to_async(cur_pairs.get_pairs_country)()
    result_inlines = []

    for country, currencies in pairs_country:
        if not currencies: continue
        buttons = [
            InlineKeyboardButton(f'{name} {float(price)}',
            callback_data=f'ad_{id}')
            for id, name, price in currencies]

        result_inlines.append(
            {
                'text' : country,
                'reply_markup' : InlineKeyboardMarkup(row_width=4).add(*buttons)
            }
        )

    return result_inlines



async def create_inline_confirmation() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton('Удалить',
            callback_data=f'DELETED'),
        InlineKeyboardButton('Отмена',
            callback_data=f'cancel'),
    )
