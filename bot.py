#!venv/bin/python
import asyncio
import logging
from utils.scheduler import start_apscheduler
import handlers
from aiogram import executor
from load_all import dp, bot
from data.config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL)
    await start_apscheduler()


async def on_startup_dev(dp):
    await start_apscheduler()


def main():
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup_dev, skip_updates=False)