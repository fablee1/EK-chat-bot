from aiogram.dispatcher.storage import FSMContext
from states.admin_states import EditPrizeAmount
from aiogram.types.message import ParseMode
from aiogram.utils.markdown import escape_md
from data.config import TRON_ADD
from utils.scheduler import add_prize_job, get_job
from utils.prize import get_add_bals, start_airdrop
from keyboards.admins import admins_kb
from filters.isAdmin import IsAdmin
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter

db = DBCommands()

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='admin_draws')
async def admin_prizes(call: types.CallbackQuery, message=False):
    if not message:
        await call.answer()
    prize = (await db.get_settings())['prize']
    prize_wallet_balances = await get_add_bals(TRON_ADD)
    msg = escape_md("Управляй розыргышами отсюда."
        f"\n\nПриз следующего розыгрыша: {prize} USDT"
        f"\nОсталось трона: {prize_wallet_balances[0]}"
        f"\nОсталось USDT: {prize_wallet_balances[1]}")
    msg_wallet = f"\n\nТвой кошелёк: [{TRON_ADD}](https://tronscan.io/#/address/{TRON_ADD})"
    f_msg = msg + msg_wallet
    job = get_job("prize_job")
    if not message:
        await call.message.edit_text(f_msg, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=await admins_kb.admin_prize_main_kb(job))
    else:
        await message.answer(f_msg, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=await admins_kb.admin_prize_main_kb(job))

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

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='change_prize_amount')
async def change_prize_amount(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    msg = "Введи новую величину приза в USDT."
    await call.message.edit_text(msg, reply_markup=await admins_kb.cancel_state_kb("cancel"))
    await EditPrizeAmount.EnterPrize.set()
    await state.update_data(m=call.message)

@dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), state=EditPrizeAmount.EnterPrize)
async def change_prize_amount(message: types.Message, state: FSMContext):
    msg = message.text
    m = (await state.get_data())['m']
    await m.delete()
    try:
        prize = float(msg)
        await db.update_prize(prize)
    except:
        m = await message.answer("Приз должен быть числом в виде 100 или 10.1 или 0.1, попробуй ещё раз!") 
        await state.update_data(m=m)
        return
    await admin_prizes(None, m)
    await state.reset_state()