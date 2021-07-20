import asyncio
from utils.scheduler import add_delete_msg_job
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter, IsReplyFilter, Text

db = DBCommands()

@dp.message_handler(ChatTypeFilter(['group', 'supergroup']), IsReplyFilter(True), Text(equals=["+"]))
async def increase_reputation(message: types.Message):
    m_from = message.from_user
    replied_to = message.reply_to_message.from_user
    if m_from.id == replied_to.id:
        m = await message.answer(f"❗️ @{m_from.username}, ты не можешь повысить рейтинг сам себе! ❗️")
    else:
        from_user = await db.get_user(m_from)
        replied_user = await db.get_user(replied_to)
        increase = await db.inc_reputation(from_user, replied_user)
        if increase:
            msg = f"🚀 @{m_from.username} поднял репутацию @{replied_to.username} до {replied_user['reputation'] + 1}! 🚀"
            m = await message.answer(msg)
            goal = await db.check_rep_goal(replied_user['reputation'] + 1)
            if goal:
                if goal['is_prize']:
                    await message.answer("🏆 " + goal['message'].format(user=f"@{replied_to.username}", rep=replied_user['reputation']+1, p_n=goal['prize_name']) + " 🏆")
                    if goal.get("custom_limit"):
                        await db.update_custom_limit(message.reply_to_message.from_user.id, goal["custom_limit"])
                else:
                    await message.answer(goal['message'].format(user=f"@{replied_to.username}", rep=replied_user['reputation']+1))
        else:
            m = await message.answer(f"🚨 @{m_from.username}, ты превысил лимит! 🚨")
    await message.delete()
    add_delete_msg_job(m)

@dp.message_handler(ChatTypeFilter(['group', 'supergroup']), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_chat_member(message: types.Message):
    new_users = message.new_chat_members
    await db.add_new_users(new_users)