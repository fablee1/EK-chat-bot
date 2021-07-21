#!venv/bin/python
import logging
from utils.scheduler import start_apscheduler
from aiogram.utils.executor import start_webhook, start_polling
from load_all import dp, bot
import handlers
from data.config import BOT_MODE, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL)
    # print(await bot.get_webhook_info())
    await start_apscheduler()


async def on_startup_dev(dp):
    await start_apscheduler()


def main():
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == "__main__":
    if BOT_MODE == "DEV":
        start_polling(dp, on_startup=on_startup_dev, skip_updates=False)
    elif BOT_MODE == "PROD":
        start_webhook(dp, WEBHOOK_PATH, host=WEBAPP_HOST, port=WEBAPP_PORT ,on_startup=on_startup)
