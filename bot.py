#!venv/bin/python
import logging
from utils.apscheduler import start_apscheduler
import handlers
from aiogram import executor
from aiogram.utils.executor import start_webhook
from load_all import dp, bot
from data.config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_startup_dev(dp):
    await start_apscheduler()


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
