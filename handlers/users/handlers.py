from aiogram.dispatcher.storage import FSMContext
from utils.db.lib import check_valid_tron_address
from states.user_states import AddWallet

from aiogram.types.message import ParseMode
from handlers.users.keyboards import back_to_prize_main, main_kb, prize_main_kb
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter, Text
from aiogram.utils.markdown import escape_md

db = DBCommands()

@dp.message_handler(ChatTypeFilter('private'), commands=["start"])
async def start(message: types.Message):
    await db.get_user(message.from_user)
    await message.answer(escape_md(f"👋 Привет, {message.from_user.full_name}!\n\n") + "🤖 Приветствуем тебя в официальном боте [Чата CryptoGallery](https://t.me/ek_cryptogallery_chat)" + escape_md("\n\n📊 Здесь ты можешь отследить свою репутацию, поучаствовать в розыгрышах и узнать граали трейдинга от @Ed_Khan"), reply_markup=await main_kb(), parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

@dp.message_handler(ChatTypeFilter('private'), Text(equals="📈 Мой рейтинг 📈"))
async def get_rating(message: types.Message):
    user_data = await db.get_user(message.from_user)
    if user_data:
        msg = f"🥇 Твоя Репутация: {user_data.get('reputation', 'нет данных')}\n\n🎖 Отдано Репутации: {user_data.get('rep_given', 'нет данных')}\n\n🎗 Осталось отдать Репутации сегодня: {user_data.get('rep_limit', 'нет данных')}\n\n\n🏆 ТОП 10 по Репутации в Чате:"
        rep_top = await db.get_rep_top()
        msg_top = "".join(map(lambda x, y: f"   {y}. @{x['username']}\n", rep_top, range(1, len(rep_top)+1)))
        f_msg = msg + '\n' + msg_top
        await message.answer(f_msg)
    else:
        await message.answer("Невозможно получить статистику сейчас, попробуйте позже!")


# Handler for info
@dp.message_handler(ChatTypeFilter('private'), Text(equals="ℹ Условия ℹ"))
async def get_terms(message: types.Message):
    msg_main = (escape_md("🎖 Получай и отдавай баллы Репутации за общение в Чате! 🙌\n"
    "Раз в сутки каждому участнику Чата даётся 3 балла Репутации – чтобы проголосовать ими за понравившийся контент или годные мысли 😎\n\n") +
    "➕ *Для этого достаточно написать '\+' \(плюсик\) в ответ на понравившееся сообщение\.*\n"
    + escape_md("⚙️ Система удалит твой плюсик через пару секунд, рейтинг автора понравившегося сообщения повысится на +1 балл.\n"
    "❗️ Копить баллы или тратить на себя нельзя.\n"
    "📝 Постите интересные мысли, собственный анализ рынка, чужие новости со своим мнением – всё, что будет полезно Народу, Чату и Отечеству!\n\n\n"
    "🎁 Достигните определённого количества баллов, чтобы разблокировать следующие достижения:\n\n"))
    msg_footer = escape_md("❗️ За спам, реферальные ссылки, попытки накрутки Репутации и прочие непотребства – ") + "*БАН\!*" + escape_md(" Эти вещи, конечно, прекрасны, но не несут общественной пользы 😄")
    prizes = await db.get_prizes()
    msg_prizes = "".join(map(lambda p: f"*{p['goal']}\.* " + escape_md(p["prize_name"]) + "\n", prizes))
    msg = msg_main + msg_prizes + "\n\n" + msg_footer
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN_V2)

# Handler for links
@dp.message_handler(ChatTypeFilter('private'), Text(equals="🔗 Ссылки 🔗"))
async def get_links(message: types.Message):
    msg_main = ("🗞 *Ниже ты можешь найти всё что связано с @Ed\_Khan*\n\n"
    "1️⃣ *Мониторинги \(аудит\) ручных стратегий:*\n"
    "   \"*[CryptoGallery: Edward K\.](https://www.equite.io/en/L37vzqo6E0)*\"\n"
    "   \"*[CryptoGallery: NA CHUI](https://www.equite.io/en/0p8IKWxW4R)*\"\n"
    "   \"*[CryptoGallery: BitMEX](https://www.equite.io/en/f5zDEbAiJq)*\"\n\n"
    "2️⃣ *Мониторинги \(аудит\) ботов:*\n"
    "   *InFractals:*\n"
    "       \"*[Mod\-1\. H4\.](https://www.equite.io/en/O3CAXQA9I8)*\""
    "   \"*[Mod\-2\. H4\.](https://www.equite.io/en/vZ7vcZWATE)*\"\n"
    "       \"*[Mod\-3\. H2\.](https://www.equite.io/en/uGlvxjyhSd)*\""
    "   \"*[Mod\-4\. H1\.](https://www.equite.io/en/HkuYPRNm-j)*\"\n"
    "       \"*[Mod\-5\. H2\.](https://www.equite.io/en/eAwwePk5aZ)*\""
    "   \"*[Mod\-6\. H1\.](https://www.equite.io/en/r_IwoP9OfV)*\"\n"
    "   *Ramm:*\n"
    "       \"*[Only BTCUSDT\.](https://www.equite.io/en/U6fl3JyB6C)*\""
    "   \"*[Mod\-1\.](https://www.equite.io/en/H6J1js-oYN)*\"\n"
    "       \"*[Mod\-2\.](https://www.equite.io/en/igeHrx0k2S)*\""
    "   \"*[Mod\-3\.](https://www.equite.io/en/1XDM4VC9Xz)*\"\n"
    "   *Utopia:*\n"
    "       \"*[Mod\-1\.](https://www.equite.io/en/O2fHjEbyPq)*\""
    "   \"*[Mod\-2\.](https://www.equite.io/en/FNEhEfdSMe)*\"\n"
    "       \"*[New\.](https://www.equite.io/en/RH77PgB6GU)*\""
    "   \"*[2 pairs\.](https://www.equite.io/en/vsQN-fwsP4)*\"\n"
    "       \"*[Half\.](https://www.equite.io/en/DCl48IJy78)*\"\n\n"
    "3️⃣ *Ссылки на блоги / сети / ресурсы:*\n"
    "   • *[Скидки на комиссии: 10% Binance Futures, 20% Binance Spot](https://www.binance.com/en/register?ref=WO4MG0K0)*\n"
    "   • *[Рейтинг Aivia \(с возможностью подключения\)](https://app.aivia.io/rankings/rNMXYTXvMb)*\n"
    "   • *[TradingView](https://ru.tradingview.com/u/Ed_Khan/)*\n"
    "   • *[Twitter](https://twitter.com/realedkhan)*")
    await message.answer(msg_main, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


# Code for Prize Handling
@dp.message_handler(ChatTypeFilter('private'), Text(equals="🎁 Розыгрыш! 🎁"))
async def participate_in_airdrop(message: types.Message, call=False):
    prize = (await db.get_settings())['prize']
    subscribed = await db.check_user_subscribed(message.chat.id)
    participating = await db.user_participating(message.chat.id)
    wallet = (await db.get_user_by_id(message.chat.id))['address']
    wallet_added = not wallet == None
    main_msg = ("🎁 Ежедневный розыгрыш от *[EK CryptoGallery](https://t.me/edkhan_cryptogallery)*\!\n\n"
                f"Сегодняшний приз *{escape_md(prize)}* USDT\.\n\n"
                f"Адрес твоего кошелька: *{wallet if wallet_added else 'не указан'}*")
    if call:
        await message.edit_text(main_msg, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=await prize_main_kb(subscribed, participating, wallet_added), disable_web_page_preview=True)
    else:
        await message.answer(main_msg, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=await prize_main_kb(subscribed, participating, wallet_added), disable_web_page_preview=True)

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
    await call.message.edit_text(main_msg, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    await call.message.edit_reply_markup(await back_to_prize_main())

@dp.callback_query_handler(ChatTypeFilter('private'), text="back_to_prize_main")
async def back_to_main(call: types.CallbackQuery):
    await call.answer()
    await participate_in_airdrop(call.message, True)

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