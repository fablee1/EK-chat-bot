from aiogram.dispatcher.storage import FSMContext
from states.admin_states import EditResetLimit
from aiogram.types.message import ParseMode
from keyboards.admins import admins_kb
from filters.isAdmin import IsAdmin
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter
from aiogram.utils.markdown import escape_md
from utils.scheduler import get_next_run_time

db = DBCommands()

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='admin_limits')
async def admin_res_limit(call: types.CallbackQuery):
    await call.answer()
    settings = await db.get_settings()
    limit = settings['rep_reset_limit']
    nrt = get_next_run_time('reset_reputation').strftime("%b %d %Y %H:%M:%S")
    msg = f"*Репутации после сброса:* {limit}\n*Следующий сброс:* {escape_md(nrt)} по Москве\."
    await call.message.edit_text(msg, parse_mode=ParseMode.MARKDOWN_V2)
    await call.message.edit_reply_markup(reply_markup=await admins_kb.admin_edit_limits_kb())

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='change_reset_limit')
async def admin_change_res_limit(call: types.CallbackQuery):
    await call.answer()
    msg = "Введи новый лимит репутации после сброса"
    await call.message.edit_text(msg)
    await call.message.edit_reply_markup(reply_markup=await admins_kb.cancel_state_kb('cancel_limit_change'))
    await EditResetLimit.EnterNumber.set()

@dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), state=EditResetLimit.EnterNumber)
async def admin_change_limit_new(message: types.Message, state: FSMContext):
    new_limit = message.text
    if not new_limit.isdigit():
        return await message.answer('Лимит должен быть числом, попробуй ещё раз или нажми отменить.', reply_markup=await admins_kb.cancel_state_kb('cancel_limit_change'))
    elif int(new_limit) <= 0:
        return await message.answer('Лимит должен быть положительным числом, попробуй ещё раз или нажми отменить.', reply_markup=await admins_kb.cancel_state_kb('cancel_limit_change'))
    msg = f"Новый лимит будет: {new_limit}\n\nНажми подтвердить или отменить."
    await message.answer(msg, reply_markup=await admins_kb.admin_confirm_limits_kb())
    await EditResetLimit.Confirm.set()
    await state.update_data(new_limit=int(new_limit))

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text="confirm_reset_limit_change", state=EditResetLimit.Confirm)
async def admin_change_limit_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    new_limit = (await state.get_data()).get('new_limit')
    await db.set_rep_reset_limit(new_limit)
    await state.reset_state()
    await admin_res_limit(call)

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text="cancel_limit_change", state=EditResetLimit)
async def admin_change_limit_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.reset_state()
    await admin_res_limit(call)