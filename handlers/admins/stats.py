from keyboards.admins import admins_kb
from filters.isAdmin import IsAdmin
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter, Text

db = DBCommands()

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='admin_stats')
async def admin_stats(call: types.CallbackQuery):
    await call.answer()
    msg = ('📊 Статистика 📊'
            '\n\n🐸 Юзеры: {u_n}'
            '\n💼 Админы: {a_l}').format(u_n=0, a_l=0)
    await call.message.edit_text(msg)
    await call.message.edit_reply_markup(reply_markup=await admins_kb.stats_back())