async def set_hook():
    import asyncio
    from data.config import HEROKU_APP_NAME, WEBHOOK_URL
    from load_all import bot

    async def hook_set():
        if not HEROKU_APP_NAME:
            print('You have forgot to set HEROKU_APP_NAME')
            quit()
        await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=False)
        print(await bot.get_webhook_info())

    asyncio.run(hook_set())
    await bot.close()


if __name__ == "__main__":
    set_hook()