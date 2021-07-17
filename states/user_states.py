from keyboards.admins.admins_kb import stats_back
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddWallet(StatesGroup):
    Confirm = State()

class EditWallet(StatesGroup):
    Confirm = State()