from aiogram.dispatcher.filters import Filter
from aiogram import types
from utils.db.database import DBCommands

db = DBCommands()

class IsAdmin(Filter):
    key = 'is_admin'

    async def check(self, message: types.Message):
        return await db.is_admin(message.from_user.id)