
from asgiref.sync import sync_to_async
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from bot.handlers.FSM import AddUserCurrencyPairs
from bot.handlers.FSM import UserDeletedPairs
from bot.buttons import inline
from aiogram.dispatcher import FSMContext

from user.models import UserPairs, UserWaiting


async def notification_change(callback: CallbackQuery, state: FSMContext):
    pairs_id = callback.data.split('_')[1]
    telegram_id = callback.from_user.id
    await AddUserCurrencyPairs.price.set()
    up = UserPairs()
    await sync_to_async(up.add_or_on_or_of)(telegram_id, pairs_id)
    async with state.proxy() as data:
        data['pairs_id'] = pairs_id

    await callback.message.answer(
        'Напишите какую цену ждем\n'\
        'Варианты ввода, сообщу когда:\n'\
        '<b> + 10</b>  : жду пока прибавит <b>10 единиц</b>\n'\
        '<b> -  5%</b>  : жду пока уменьшиться на <b>5%</b>\n'\
        '<b>    23</b>    : жду пока будет <b>23 единиц</b>\n'\
        'отмена /cancel'
        )
    await callback.answer('Жду цену')


async def follow_price(callback: CallbackQuery):
    u_id = callback.from_user.id
    pairs_id = callback.data.split('_')[1]
    up = UserPairs()
    is_daily_report = await sync_to_async(
        up.add_or_on_or_of)(u_id, pairs_id)
    mes = 'включены' if is_daily_report else 'выключены'
    await callback.answer(f'Ежедневные уведомления {mes}!')


async def deleted_pairs_for_user(
    callback: CallbackQuery,
    state: FSMContext
    ):
    telegram_id = callback.from_user.id
    async with state.proxy() as data:
        pairs_id = data['pairs_id']
    uw = UserWaiting()
    up = UserPairs()
    params = {
        'user' : telegram_id,
        'pairs' : pairs_id
    }
    await sync_to_async(uw.delete_by_param)(params)
    await sync_to_async(up.delete_by_param)(params)
    await callback.answer(
        'Удалил валютную пару и все ожидания цены!'
        )


async def deleted_user_watching(callback: CallbackQuery):
    uw_id = callback.data.split('_')[1]
    telegram_id = callback.from_user.id
    uw = UserWaiting()
    await sync_to_async(uw.delete_by_param)(
            {'id' : uw_id,}
        )

    await callback.answer('Удалил ожидание цены')


async def deletion_confirmation_pairs_for_user(
    callback: CallbackQuery,
    state: FSMContext
    ):
    pairs_id = callback.data.split('_')[1]
    await UserDeletedPairs.answer.set()
    async with state.proxy() as data:
        data['pairs_id'] = pairs_id
    buttons = await inline.create_inline_confirmation()
    await callback.message.answer(
        text='Удалить валютную пару и все ожидания цены?',
        reply_markup=buttons
    )
    await callback.answer('Уверен?')



async def cancel_handler(callback: CallbackQuery,
    state: FSMContext
    ):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.answer('Ок!')


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        notification_change, Text(startswith='ad_'))

    dp.register_callback_query_handler(
        follow_price, Text(startswith='fp_'))

    dp.register_callback_query_handler(
        deletion_confirmation_pairs_for_user, Text(startswith='DP_'))
    dp.register_callback_query_handler(
        deleted_user_watching, Text(startswith='DUW_'))

    dp.register_callback_query_handler(
        cancel_handler, Text(equals='cancel'), state='*')
    dp.register_callback_query_handler(
        deleted_pairs_for_user, state=UserDeletedPairs.answer)
