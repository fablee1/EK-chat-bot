import asyncio
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
        m = await message.answer(f"@{m_from.username}, ты не можешь повысить рейтинг сам себе!")
    else:
        from_user = await db.get_user(m_from)
        replied_user = await db.get_user(replied_to)
        increase = await db.inc_reputation(from_user, replied_user)
        if increase:
            msg = f"@{m_from.username} поднял репутацию @{replied_to.username} до {replied_user['reputation'] + 1}!"
            m = await message.answer(msg)
            goal = await db.check_rep_goal(replied_user['reputation'] + 1)
            if goal:
                await message.answer(goal['message'].format(user=f"@{replied_to.username}"))
        else:
            m = await message.answer(f"@{m_from.username}, ты превысил лимит!")
    await asyncio.sleep(5)
    await m.delete()

@dp.message_handler(ChatTypeFilter(['group', 'supergroup']), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_chat_member(message: types.Message):
    new_users = message.new_chat_members
    await db.add_new_users(new_users)

# @dp.message_handler(ChatTypeFilter(['group', 'supergroup']), commands=["reset"])
# async def reset_limits(message: types.Message):
#     await message.answer(f"Успешно запущен сброс лимитов каждые 60 секунд!")
