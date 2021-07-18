from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

congrats_list_cb = CallbackData('congrats_list', 'page', sep=';')
congrats_choose_is_prize_cb = CallbackData('congrats_choose_is_prize', 'action', sep=';')
congrats_edit_is_prize_cb = CallbackData('congrats_edit_is_prize_cb', 'action', sep=';')

async def admin_kb():
    admin_main_kb = InlineKeyboardMarkup(row_width=2)
    button_rows = [
        [
            InlineKeyboardButton('Поздравления', callback_data='admin_congrats'),
            InlineKeyboardButton('Розыгрыши', callback_data='admin_draws')
        ],
        [
            InlineKeyboardButton('Лимиты', callback_data='admin_limits'),
            InlineKeyboardButton('Статистика', callback_data='admin_stats')
        ],
        InlineKeyboardButton('Выйти из админ панели', callback_data='admin_exit_panel')
    ]
    for x in button_rows:
        if type(x) is list:
            admin_main_kb.add(x[0])
            for b in x[1:]:
                admin_main_kb.insert(b)
        else:
            admin_main_kb.add(x)
    return admin_main_kb

async def stats_back():
    stats_back_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton('Назад', callback_data='back_to_admin_main')
    )
    return stats_back_kb


async def congrats_menu_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Добавить поздравление', callback_data='congrats_add'))
    kb.add(InlineKeyboardButton('Редактировать поздравление', callback_data='congrats_edit'))
    kb.add(InlineKeyboardButton('Список поздравлений', callback_data=congrats_list_cb.new(page=0)))
    kb.add(InlineKeyboardButton('Назад', callback_data='back_to_admin_main'))
    return kb

async def congrats_list_pagination_kb(page, is_last=False):
    kb = InlineKeyboardMarkup()
    if page > 0:
        kb.add(InlineKeyboardButton('⬅️', callback_data=congrats_list_cb.new(page=page-1)))
    if not is_last:
        kb.insert(InlineKeyboardButton('➡️', callback_data=congrats_list_cb.new(page=page+1)))
    kb.add(InlineKeyboardButton('Назад в меню', callback_data="admin_congrats"))
    return kb

async def cancel_state_kb(callback):
    kb=InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Отменить', callback_data=callback))
    return kb

async def choose_is_prize_kb():
    kb=InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Да, призовой ✅', callback_data=congrats_choose_is_prize_cb.new(action='true')))
    kb.add(InlineKeyboardButton('Не призовой ❌', callback_data=congrats_choose_is_prize_cb.new(action='false')))
    kb.add(InlineKeyboardButton('Отменить', callback_data='congrats_cancel'))
    return kb

async def сonfirm_add_congrats_kb():
    kb=InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Всё правильно!', callback_data='confirm_add_congrats'))
    kb.add(InlineKeyboardButton('Начать заново!', callback_data='reset_add_congrats'))
    kb.add(InlineKeyboardButton('Отменить', callback_data='congrats_add_cancel'))
    return kb

async def edit_congrats_main_kb(is_prize):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Не призовой ❌' if not is_prize else 'Призовой ✅', callback_data=congrats_edit_is_prize_cb.new(action=is_prize)))
    if is_prize:
        kb.add(InlineKeyboardButton('Изменить название приза', callback_data='edit_congrats_prize_name'))
    kb.add(InlineKeyboardButton('Изменить кол. репутации', callback_data='edit_congrats_goal'))
    kb.add(InlineKeyboardButton('Изменить сообщение', callback_data='edit_congrats_message'))
    kb.add(InlineKeyboardButton('Назад', callback_data='congrats_cancel'))
    return kb

async def admin_edit_limits_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Поменять лимит репутации', callback_data="change_reset_limit"))
    kb.add(InlineKeyboardButton('Назад', callback_data='back_to_admin_main'))
    return kb

async def admin_confirm_limits_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Подтвердить', callback_data="confirm_reset_limit_change"))
    kb.add(InlineKeyboardButton('Назад', callback_data='cancel_limit_change'))
    return kb

async def admin_prize_main_kb(running=False):
    kb = InlineKeyboardMarkup()
    if running:
        kb.add(InlineKeyboardButton('Остановить розыгрыши!', callback_data="stop_raffles"))
    else:
        kb.add(InlineKeyboardButton('Возобновить розыгрыши!', callback_data="schedule_raffles"))
    kb.add(InlineKeyboardButton('Запустить розыгрыш сейчас', callback_data="launch_prize_now"))
    kb.add(InlineKeyboardButton('Назад', callback_data='back_to_admin_main'))
    return kb