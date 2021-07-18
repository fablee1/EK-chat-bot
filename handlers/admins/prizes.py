from utils.apscheduler import add_prize_job, get_job
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
    job = get_job("prize_job")
    await call.message.edit_text(msg)
    await call.message.edit_reply_markup(await admins_kb.admin_prize_main_kb(job))

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='launch_prize_now')
async def admin_prize_launch_now(call: types.CallbackQuery):
    await call.answer()
    msg = "Запущен розыгрыш!"
    await call.message.answer(msg)
    await start_airdrop()

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='stop_raffles')
async def stop_raffles(call: types.CallbackQuery):
    await call.answer()
    get_job("prize_job").remove()
    await admin_prizes(call)

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='schedule_raffles')
async def schedule_raffles(call: types.CallbackQuery):
    await call.answer()
    add_prize_job(start_airdrop)
    await admin_prizes(call)