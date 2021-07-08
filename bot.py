#!venv/bin/python
import logging

from aiogram import executor
from aiogram.utils.executor import start_webhook
from load_all import dp, bot
import handlers
# from database import create_db
from data.config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    # await create_db()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_startup_dev(dp):
    print('started polling')
    # await create_db()


def main():
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup_dev, skip_updates=True)
