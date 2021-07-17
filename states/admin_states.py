from aiogram.dispatcher.filters.state import State, StatesGroup


class AddCongrats(StatesGroup):
    EnterRep = State()
    IsPrize = State()
    EnterMessage = State()
    Confirm = State()

class EditCongrats(StatesGroup):
    EnterNumber = State()
    EditMenu = State()
    EditGoal = State()
    EditMessage = State()
    EditPrizeName = State()

class EditResetLimit(StatesGroup):
    EnterNumber = State()
    Confirm = State()