import asyncio
from handlers.users.keyboards import main_kb
from utils.db.database import DBCommands
from aiogram import types
from load_all import dp
from aiogram.dispatcher.filters.builtin import ChatTypeFilter, Text

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