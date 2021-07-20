
from keyboards.admins.admins_kb import to_bot_kb
from data.config import DB_CONN, MAIN_CHAT_ID
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pymongo import MongoClient
from utils.db.database import DBCommands
from load_all import bot

db = DBCommands()

MClient = MongoClient(DB_CONN)

jobstores = {
    'default': MongoDBJobStore(database="EK-CHAT-BOT", collection="apscheduler", client=MClient),
}

scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="Europe/Moscow")

async def reset_limit():
    settings = await db.get_settings()
    await db.reset_rep_limits(settings['rep_reset_limit'])

async def reset_custom_limits():
    await db.reset_custom_limits()

def get_job(id):
    job = scheduler.get_job(id)
    return job

def get_next_run_time(id):
    next_run_time = get_job(id).next_run_time
    return next_run_time

def add_prize_job(function):
    scheduler.add_job(function, trigger='cron', hour=20, id="prize_job", replace_existing=True, misfire_grace_time=60*60*12)

async def remind_rep():
    msg = ("🥇 В нашем Чате действует система Репутации.\n\n"
        "📝 Пиши полезный контент, и если он понравится другим пользователям, ты получишь от них баллы.\n\n"
        "🏆 За определённую Репутацию полагаются награды!\n\n"
        "🧾 Подробнее читай в Условиях:")
    await bot.send_message(MAIN_CHAT_ID, msg, reply_markup=await to_bot_kb())

async def remind_prize():
    prize = (await db.get_settings()).get('prize')
    msg = (f"💰 Напоминаю о ежедневном розыгрыше {prize} USDT среди пользователей Чата!\n\n"
        "🤖 Участвуй, нажав кнопку «Розыгрыш»!")
    await bot.send_message(MAIN_CHAT_ID, msg, reply_markup=await to_bot_kb())


async def start_apscheduler():
    scheduler.start()
    

# scheduler.add_job(reset_custom_limits, trigger='cron', hour=00, id="reset_custom_limits", replace_existing=True, misfire_grace_time=60*60*12)
# scheduler.add_job(reset_limit, trigger='cron', hour=00, id="reset_reputation", replace_existing=True, misfire_grace_time=60*60*12)
# scheduler.add_job(remind_rep, trigger='cron', hour=13, id="remind_rep", replace_existing=True, misfire_grace_time=60*60*12)
# scheduler.add_job(remind_prize, trigger='cron', hour=18, id="remind_prize", replace_existing=True, misfire_grace_time=60*60*12)