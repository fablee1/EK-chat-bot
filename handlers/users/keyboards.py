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
               KeyboardButton('🎁 Участвовать в розыгрыше! 🎁')
            ],
            [
                KeyboardButton('🔗 Ссылки'),
                KeyboardButton('👛 Кошелёк')
            ],
        ], resize_keyboard=True
    )
    return kb