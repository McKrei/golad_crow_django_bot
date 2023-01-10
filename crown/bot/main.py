from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.message import register_all_handlers
from bot.handlers.callback import register_callback_handlers
from env import TOKEN

bot = Bot(token=TOKEN, parse_mode='HTML')


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_handlers(dp)
    register_callback_handlers(dp)


def runbot():
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
