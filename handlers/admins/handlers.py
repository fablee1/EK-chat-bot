import asyncio
from keyboards.admins import admins_kb
from filters.isAdmin import IsAdmin
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp, bot
from aiogram.dispatcher.filters.builtin import ChatTypeFilter, ForwardedMessageFilter, Text

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

# @dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), ForwardedMessageFilter(True))
# async def get_info_about_forward(message: types.Message):
    # for x in range(1000):
    #     try:
    #         await bot.get_chat_member(694669934, 694669934)
    #         is_in = True
    #     except:
    #         is_in = False
    #     await message.answer(is_in)
    #     await asyncio.sleep(0.1)