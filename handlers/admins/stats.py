from keyboards.admins import admins_kb
from filters.isAdmin import IsAdmin
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter, Text

db = DBCommands()

@dp.callback_query_handler(ChatTypeFilter(['private']), IsAdmin(), text='admin_stats')
async def admin_stats(call: types.CallbackQuery):
    await call.answer()
    stats = await db.admin_get_stats()
    u_stats = stats[0][0]
    p_stats = stats[1][0]
    msg = ('📊 Статистика 📊'
            '\n\n🗿 Юзеры: {u_n}'
            '\n🌝 Всего репутации отдано: {rep_t}'
            '\n📈 Макс. репутации у юзера: {max_r}'
            '\n\n💵 Всего призов разыграно: {prizes_t}'
            '\n💰 Денег разыграно: {prizes_sum}'
            ).format(u_n=u_stats['user_count'], rep_t=u_stats['total_rep_given'], max_r=u_stats['max_rep'],
                        prizes_t=p_stats['total_raffles'], prizes_sum=round(p_stats['total_prize_sum'], 2))
    await call.message.edit_text(msg)
    await call.message.edit_reply_markup(reply_markup=await admins_kb.stats_back())