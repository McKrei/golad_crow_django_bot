
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from bot.handlers.FSM import AddUserCurrencyPairs
from bot.buttons import inline
from bot.buttons.keyboards import only_menu
from util.add_data import add_user_waiting


async def get_start(msg: Message):
    mes = 'Привет, я могу следить за ценой валюты'
    mes = '\nна сайте золотой короны\n и уведомлять тебя об изменениях'
    mes += '\n<b>Нашел ошибку пиши:</b> https://t.me/McKrei'
    await msg.answer(
        mes,
        reply_markup=only_menu)


async def all_currency(msg: Message):
    user = msg.from_user.id
    all_buttons = await inline.get_all_buttons_currency()
    for button in all_buttons:
        await msg.answer(**button)


async def my_currency(msg: Message):
    user = msg.from_user.id
    inlines = await inline.get_all_buttons_my_currency(user)
    if inlines:
        for button in inlines:
            await msg.answer(**button)


async def notification_change_save(msg: Message, state: FSMContext):
    user = msg.from_user.id
    async with state.proxy() as data:
        pairs_id = data['pairs_id']
    result, message = await add_user_waiting(user, pairs_id, msg.text)
    if not result:
        return await msg.answer(
            f'{message}\nПопробуй еще, или жми /cancel',
            reply_markup=only_menu
        )

    await msg.answer(f'{message}', reply_markup=only_menu)
    await state.finish()


async def cancel_handler(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.reply('Ок!')


async def other_answer(msg):
    await msg.answer('Не понимаю /help')


def register_all_handlers(dp: Dispatcher):
    dp.register_message_handler(get_start, commands=['start', 'help'])
    dp.register_message_handler(all_currency, Text(equals='Все валюты'))
    dp.register_message_handler(my_currency, Text(equals='Слежу'))
    dp.register_message_handler(
        cancel_handler, commands=['cancel'], state='*')
    dp.register_message_handler(
        cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(
        notification_change_save, state=AddUserCurrencyPairs.price)


    dp.register_message_handler(other_answer)
