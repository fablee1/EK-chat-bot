from keyboards.admins import admins_kb
from filters.isAdmin import IsAdmin
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter, Text

db = DBCommands()

@dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), commands=["admin"])
async def enter_admin_panel(message: types.Message):
    user = types.User.get_current()
    msg = ('Привет, {name}.\n\n'
            'Используя меню ниже, ты можешь '
            'настраивать бота, следить за розыгрышами, '
            'и посматривать на статистику.').format(name=user.full_name)
    await message.delete()
    await message.answer(msg, reply_markup=await admins_kb.admin_kb())

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='admin_exit_panel')
async def exit_admin_panel(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='back_to_admin_main')
async def admin_stats_back(call: types.CallbackQuery):
    await call.answer()
    await enter_admin_panel(call.message)