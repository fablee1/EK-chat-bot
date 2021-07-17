from utils.prize import start_airdrop
from keyboards.admins import admins_kb
from filters.isAdmin import IsAdmin
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter

db = DBCommands()

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='admin_draws')
async def admin_prizes(call: types.CallbackQuery):
    await call.answer()
    msg = "Меню призов, дальше ещё не придумал:D"
    await call.message.edit_text(msg)
    await call.message.edit_reply_markup(await admins_kb.admin_prize_main_kb())

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='launch_prize_now')
async def admin_prize_launch_now(call: types.CallbackQuery):
    await call.answer()
    msg = "Запущен розыгрыш!"
    await call.message.answer(msg)
    await start_airdrop()