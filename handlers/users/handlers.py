import asyncio

from aiogram.dispatcher.storage import FSMContext
from utils.db.lib import check_valid_tron_address
from states.user_states import AddWallet

from aiogram.types.message import ParseMode
from six import text_type
from handlers.users.keyboards import main_kb, prize_main_kb
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter, Text
from aiogram.utils.markdown import escape_md

db = DBCommands()

@dp.message_handler(ChatTypeFilter('private'), commands=["start"])
async def start(message: types.Message):
    await db.get_user(message.from_user)
    await message.answer(f"Привет, {message.from_user.full_name}! Приветствуем тебя в официальном боте чата @ek_cryptogallery_chat", reply_markup=await main_kb())

@dp.message_handler(ChatTypeFilter('private'), Text(equals="📈 Мой рейтинг"))
async def get_rating(message: types.Message):
    user_data = await db.get_user(message.from_user)
    if user_data:
        msg = f"Твоя репутация: {user_data.get('reputation', 'нет данных')}\nОтдано репутации: {user_data.get('rep_given', 'нет данных')}\nОсталось очков отдать сегодня: {user_data.get('rep_limit', 'нет данных')}"
        await message.answer(msg)
    else:
        await message.answer("Невозможно получить статистику сейчас, попробуйте позже!")


# Code for Prize Handling
@dp.message_handler(ChatTypeFilter('private'), Text(equals="🎁 Розыгрыш! 🎁"))
async def participate_in_airdrop(message: types.Message):
    prize = (await db.get_settings())['prize']
    subscribed = await db.check_user_subscribed(message.from_user.id)
    participating = await db.user_participating(message.from_user.id)
    wallet_added = not (await db.get_user_by_id(message.from_user.id))['address'] == None
    main_msg = ("🎁 Ежедневный розыгрыш от *[EK Cryptogallery](https://t.me/edkhan_cryptogallery)*\!\n\n"
                f"Сегодняшний приз *{escape_md(prize)}* USDT\.")
    await message.answer(main_msg, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=await prize_main_kb(subscribed, participating, wallet_added))

@dp.callback_query_handler(ChatTypeFilter('private'), text="prize_rules")
async def prize_rules(call: types.CallbackQuery):
    await call.answer()
    main_msg = ("Правила:\n\n"
                "*1️⃣* Чтобы участвовать надо быть подписанным на *[чат](https://t.me/ek_cryptogallery_chat)* и *[канал](https://t.me/edkhan_cryptogallery)*\!\n\n"
                "*2️⃣* Если на момент розыгрыша, участник не подписан на какой либо ресурс, то он исключается из розыгрыша\.\n\n"
                "*3️⃣* Раз в сутки \(в 20\.00 по Мск\) будет выбираться победитель\.\n\n"
                "*4️⃣* Чтобы забрать приз надо прикрепить свой кошелёк USDT TRC20\.\n\n"
                "*5️⃣* Если ты выиграл, тебе придёт сообщение с кнопкой забрать приз\.\n\n"
                "*6️⃣* Убедись что кошелёк правильный, и не забудь что у тебя только 24 часа чтобы забрать приз\!"
    )
    await call.message.edit_text(main_msg, parse_mode=ParseMode.MARKDOWN_V2)

@dp.callback_query_handler(ChatTypeFilter('private'), text="participate")
async def participate_action(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Спасибо за участие! Жди результатов!")
    await call.message.delete()
    await db.user_participate(call.from_user.id)

@dp.callback_query_handler(ChatTypeFilter('private'), text="check_subscribed")
async def check_subscriptions_action(call: types.CallbackQuery):
    subscribed = await db.check_user_subscribed(call.from_user.id)
    if subscribed:
        await call.answer('Ты подписался! Теперь нажми на кнопку участвовать!', show_alert=True)
    else:
        await call.answer('Ты ещё не подписан!', show_alert=True)
    user = await types.User.get_current()
    participating = await db.user_participating(user.id)
    wallet_added = not (await db.get_user_by_id(user.id))['address'] == None
    await call.message.edit_reply_markup(await prize_main_kb(subscribed, participating, wallet_added))

@dp.callback_query_handler(ChatTypeFilter('private'), text="already_participating")
async def already_participating(call: types.CallbackQuery):
    await call.answer("Ты уже участвуешь!", show_alert=True)
    await call.message.delete()

@dp.callback_query_handler(ChatTypeFilter('private'), text="add_wallet")
async def add_wallet(call: types.CallbackQuery):
    await call.answer()
    msg = "Призы высылаются в виде USDT токенов в сети TRC20, поэтому введи адрес кошелька который поддерживает TRC20 токены."
    await call.message.edit_text(msg)
    await AddWallet.Confirm.set()

@dp.message_handler(ChatTypeFilter('private'), state=AddWallet.Confirm)
async def confirm_wallet(message: types.Message, state: FSMContext):
    wallet = message.text.strip()
    if not check_valid_tron_address(wallet):
        return await message.answer("Неверный формат кошелька, убедись что он правильный и попробуй ещё раз.")
    await db.add_tron_wallet(message.from_user.id, wallet)
    await state.reset_state()
    await participate_in_airdrop(message)