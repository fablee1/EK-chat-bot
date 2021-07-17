from load_all import bot

async def write_message(to, message):
    await bot.send_message(to, message)