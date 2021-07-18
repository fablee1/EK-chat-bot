from data.config import DB_CONN
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pymongo import MongoClient
from utils.db.database import DBCommands

db = DBCommands()

MClient = MongoClient(DB_CONN)

jobstores = {
    'default': MongoDBJobStore(database="EK-CHAT-BOT", collection="apscheduler", client=MClient),
}

scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="Europe/Moscow")

async def reset_limit():
    settings = await db.get_settings()
    await db.reset_rep_limits(settings['rep_reset_limit'])

def get_job(id):
    job = scheduler.get_job(id)
    return job

def get_next_run_time(id):
    next_run_time = get_job(id).next_run_time
    return next_run_time

def add_prize_job(function):
    scheduler.add_job(function, trigger='cron', hour=20, id="prize_job", replace_existing=True, misfire_grace_time=60*60*12)


async def start_apscheduler():
    scheduler.start()
    