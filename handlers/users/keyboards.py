from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

async def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton('📈 Мой рейтинг 📈'),
                KeyboardButton('ℹ Условия ℹ')
            ],
            [
               KeyboardButton('🎁 Розыгрыш! 🎁'),
               KeyboardButton('🔗 Ссылки 🔗'),
            ],
        ], resize_keyboard=True
    )
    return kb

async def prize_main_kb(subscribed, participating, address):
    kb = InlineKeyboardMarkup()
    if not subscribed:
        kb.add(InlineKeyboardButton('Проверить подписки', callback_data="check_subscribed"))
    elif not address:
        kb.add(InlineKeyboardButton('Добавить кошелёк', callback_data="add_wallet"))
    elif not participating:
        kb.add(InlineKeyboardButton('Участвовать', callback_data="participate"))
    else:
        kb.add(InlineKeyboardButton('Ты уже участвуешь!', callback_data="already_participating"))
    kb.add(InlineKeyboardButton('Правила', callback_data="prize_rules"))
    if address:
        kb.add(InlineKeyboardButton('Изменить кошелёк', callback_data="add_wallet"))
    return kb

async def chat_prize_trans(transaction_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Посмотреть транзакцию", url="https://tronscan.io/#/transaction/" + transaction_id))
    return kb