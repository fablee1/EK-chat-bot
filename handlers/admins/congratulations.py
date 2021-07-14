from utils.db.models import AchievementModel
from aiogram.dispatcher.storage import FSMContext
from states.admin_states import AddCongrats, EditCongrats
from aiogram.types.message import ParseMode
from keyboards.admins import admins_kb
from filters.isAdmin import IsAdmin
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter
from aiogram.utils.markdown import escape_md

db = DBCommands()

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='admin_congrats')
async def admin_congrats(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Выбери что хочешь сделать с поздравлениями.')
    await call.message.edit_reply_markup(reply_markup=await admins_kb.congrats_menu_kb())


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), admins_kb.congrats_list_cb.filter())
async def congrats_list(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    page = int(callback_data['page'])
    congrats_list = await db.get_congrats(page)
    is_last_page = True
    if len(congrats_list) == 6:
        is_last_page = False

    nl = '\n'
    msg_main = "\n\n".join(list(map(lambda x: f"*Репутации надо:* {x['goal']}\n*Призовой:* {'✅' if x.get('is_prize') else '❌'}{'{nl}*Название приза:* {p_name}'.format(p_name=(escape_md(x.get('prize_name'))), nl=nl) if x.get('is_prize') else ''}\n*Сообщение:* {escape_md(x['message'])}", congrats_list)))
    msg = "*Список всех поздравлений\.*\n\n\n" + msg_main

    await call.message.edit_text(msg, parse_mode=ParseMode.MARKDOWN_V2)
    await call.message.edit_reply_markup(reply_markup=await admins_kb.congrats_list_pagination_kb(page, is_last_page))


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='admin_congrats')
async def admin_congrats(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Выбери что хочешь сделать с поздравлениями.')
    await call.message.edit_reply_markup(reply_markup=await admins_kb.congrats_menu_kb())


# -------------- add congrats --------------------
@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text="congrats_cancel", state=AddCongrats)
async def cancel_congrats(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await admin_congrats(call)
    await state.reset_state()


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text="congrats_add")
async def add_congrats(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(("Введи необходимое количество репутации, "
                                    "для этого поздравления.\n\nИли нажми отменить, чтобы вернуться в меню."))
    await call.message.edit_reply_markup(reply_markup=await admins_kb.cancel_state_kb('congrats_cancel'))
    await AddCongrats.EnterRep.set()


@dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), state=AddCongrats.EnterRep)
async def enter_congrats_rep(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        goal = int(message.text)
    else:
        return await message.answer('Число должно быть целым и положительным, попробуй ещё раз!', reply_markup=await admins_kb.cancel_state_kb('congrats_cancel'))
    new_goal_unique = await db.check_congrat_unique(goal)
    if not new_goal_unique:
        return await message.answer('Поздравление с такой целью уже существует, выбери другое число.', reply_markup=await admins_kb.cancel_state_kb('congrats_cancel'))
    achievement = AchievementModel()
    achievement.goal = goal
    await message.answer(f'Необходимо репутации: {goal}\nТеперь выбери призовое ли поздравление, или нажми отменить.',
                        reply_markup=await admins_kb.choose_is_prize_kb())
    await AddCongrats.IsPrize.set()
    await state.update_data(achievement=achievement)


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), admins_kb.congrats_choose_is_prize_cb.filter(), state=AddCongrats.IsPrize)
async def choose_congrats_is_prize(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    is_prize = callback_data['action']
    achievement = (await state.get_data()).get('achievement')
    if is_prize == 'true':
        achievement.is_prize = True
    else:
        achievement.is_prize = False
    await call.answer()
    await call.message.answer(f"Поздравление призовое: {'✅' if is_prize == 'true' else '❌'}\nТеперь введи сообщение при поздравлении, или нажми отменить.",
                        reply_markup=await admins_kb.cancel_state_kb('congrats_cancel'))
    await AddCongrats.EnterMessage.set()
    await state.update_data(achievement=achievement)
    

@dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), state=AddCongrats.EnterMessage)
async def choose_congrats_is_prize(message: types.Message, state: FSMContext):
    congrats_text = message.text
    achievement = (await state.get_data()).get('achievement')
    achievement.message = congrats_text
    await message.answer(f"Сообщение поздравления: {congrats_text}\nТеперь подтверди что всё правильно, начни заново или нажми отменить.",
                        reply_markup=await admins_kb.сonfirm_add_congrats_kb())
    await AddCongrats.Confirm.set()
    await state.update_data(achievement=achievement)


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), state=AddCongrats.Confirm)
async def confirm_add_congrats(call: types.CallbackQuery, state: FSMContext):
    action = call.data
    await call.answer()
    if action == 'confirm_add_congrats':
        achievement = (await state.get_data()).get('achievement')
        await db.add_new_congrats(achievement)
    elif action == 'reset_add_congrats':
        await state.reset_state()
        return await add_congrats(call)
    await state.reset_state()
    await admin_congrats(call)


# -------------- add congrats --------------------

# -------------- edit congrats --------------------
@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text="congrats_cancel", state=EditCongrats)
async def cancel_congrats(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await admin_congrats(call)
    await state.reset_state()


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text="congrats_edit")
async def edit_congrat(call: types.CallbackQuery):
    await call.answer()
    msg = "Введи необходимое количество репутации, от поздравления которое хочешь отредактировать, либо нажми отменить."
    await call.message.edit_text(msg)
    await call.message.edit_reply_markup(reply_markup=await admins_kb.cancel_state_kb('congrats_cancel'))
    await EditCongrats.EnterNumber.set()


@dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), state=EditCongrats.EnterNumber)
async def get_edit_congrats(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        goal = int(message.text)
    else:

        return await message.answer('Число должно быть целым и положительным, попробуй ещё раз!')
    goal_exists = await db.get_single_congrats(goal)
    if not goal_exists:
        return await message.answer(f"Поздравления с количеством репутации {goal} не существует!")
    msg = f"Необходимое количество репутации: {goal}\n\nСообщение по достижению: {goal_exists['message']}"
    await message.answer(msg, reply_markup=await admins_kb.edit_congrats_main_kb(goal_exists['is_prize']))
    await EditCongrats.EditMenu.set()
    await state.update_data(achievement=goal_exists)


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), admins_kb.congrats_edit_is_prize_cb.filter(), state=EditCongrats.EditMenu)
async def edit_congrats_is_prize(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    goal = (await state.get_data()).get('achievement')['goal']
    is_prize = callback_data['action']
    await db.update_congrats_is_prize(goal, True if is_prize == 'False' else False)
    call.message.text = str(goal)
    await call.message.delete()
    await EditCongrats.EnterNumber.set()
    await get_edit_congrats(call.message, state)


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='edit_congrats_goal', state=EditCongrats.EditMenu)
async def edit_congrats_goal(call: types.CallbackQuery):
    await call.answer()
    msg = "Введи новое необходимое количество репутации для этого поздравления, или нажми отменить."
    await call.message.edit_text(msg)
    await call.message.edit_reply_markup(reply_markup=await admins_kb.cancel_state_kb('congrats_cancel'))
    await EditCongrats.EditGoal.set()


@dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), state=EditCongrats.EditGoal)
async def confirm_edit_congrats_goal(message: types.Message, state: FSMContext):
    new_goal = message.text
    if new_goal.isdigit():
        new_goal = int(new_goal)
    else:
        return await message.answer('Число должно быть целым и положительным, попробуй ещё раз!')
    new_goal_unique = await db.check_congrat_unique(new_goal)
    if not new_goal_unique:
        return await message.answer('Поздравление с такой целью уже существует, выбери другое число.')
    goal = (await state.get_data()).get('achievement')['goal']
    await db.update_congrats_goal(goal, new_goal)
    await message.delete()
    await EditCongrats.EnterNumber.set()
    message.text = str(new_goal)
    await get_edit_congrats(message, state)


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='edit_congrats_message', state=EditCongrats.EditMenu)
async def edit_congrats_message(call: types.CallbackQuery):
    await call.answer()
    msg = "Введи новое сообщение поздравления, или нажми отменить."
    await call.message.edit_text(msg)
    await call.message.edit_reply_markup(reply_markup=await admins_kb.cancel_state_kb('congrats_cancel'))
    await EditCongrats.EditMessage.set()


@dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), state=EditCongrats.EditMessage)
async def confirm_edit_congrats_message(message: types.Message, state: FSMContext):
    new_message = message.text
    goal = (await state.get_data()).get('achievement')['goal']
    await db.update_congrats_message(goal, new_message)
    await message.delete()
    await EditCongrats.EnterNumber.set()
    message.text = str(goal)
    await get_edit_congrats(message, state)


@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='edit_congrats_prize_name', state=EditCongrats.EditMenu)
async def edit_congrats_prize_message(call: types.CallbackQuery):
    await call.answer()
    msg = "Введи новое сообщение поздравления, или нажми отменить."
    await call.message.edit_text(msg)
    await call.message.edit_reply_markup(reply_markup=await admins_kb.cancel_state_kb('congrats_cancel'))
    await EditCongrats.EditPrizeName.set()


@dp.message_handler(ChatTypeFilter(['private']), IsAdmin(), state=EditCongrats.EditPrizeName)
async def confirm_edit_congrats_prize_message(message: types.Message, state: FSMContext):
    new_prize_name = message.text
    goal = (await state.get_data()).get('achievement')['goal']
    await db.update_congrats_prize_name(goal, new_prize_name)
    await message.delete()
    await EditCongrats.EnterNumber.set()
    message.text = str(goal)
    await get_edit_congrats(message, state)