from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

async def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton('📈 Мой рейтинг'),
                KeyboardButton('ℹ Инфо')
            ],
            [
               KeyboardButton('🎁 Розыгрыш! 🎁')
            ],
            [
                KeyboardButton('🔗 Ссылки'),
                KeyboardButton('👛 Кошелёк')
            ],
        ], resize_keyboard=True
    )
    return kb

async def prize_main_kb(subscribed, participating):
    kb = InlineKeyboardMarkup()
    if not subscribed:
        kb.add(InlineKeyboardButton('Проверить подписки', callback_data="check_subscribed"))
    elif not participating:
        kb.add(InlineKeyboardButton('Участвовать', callback_data="participate"))
    else:
        kb.add(InlineKeyboardButton('Ты уже участвуешь!', callback_data="already_participating"))
    return kb