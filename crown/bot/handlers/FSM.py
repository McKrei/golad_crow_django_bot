from aiogram.dispatcher.filters.state import State, StatesGroup


class AddUserCurrencyPairs(StatesGroup):
        price = State()


class UserDeletedPairs(StatesGroup):
        answer = State()
