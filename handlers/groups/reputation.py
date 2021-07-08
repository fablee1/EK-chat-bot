from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter, Text

@dp.message_handler(ChatTypeFilter('group'), Text(contains=["+"]))
async def increase_reputation(message: types.Message):
    await message.reply('This is a message in a group!')