from asyncio import sleep
from datetime import datetime
from utils.db.models import PrizeModel, UserModel
from data.config import DB_CONN, MAIN_CHAT_ID, TO_SUBSCRIBE
import motor.motor_asyncio
from load_all import bot

db = motor.motor_asyncio.AsyncIOMotorClient(DB_CONN)["EK-CHAT-BOT"]

Users = db.users
Goals = db.goals
Settings = db.settings
Prizes = db.prizes


class DBCommands:
    async def add_new_users(self, users):
        try:
            await Users.insert_many([UserModel(user.id, user.full_name, user.username).__dict__ for user in users], ordered=False)
        except:
            pass

    async def add_new_user(self, user):
        user_in_chat = None
        try:
            user_in_chat = await bot.get_chat_member(MAIN_CHAT_ID, user.id)
        except:
            user_in_chat = False
        if user_in_chat:
            new_user = UserModel(user.id, user.full_name, user.username, limit=3, createdAt=datetime(2021, 1, 1)).__dict__
            user_new = await Users.insert_one(new_user)
        else:
            new_user = UserModel(user.id, user.full_name, user.username).__dict__
            user_new = await Users.insert_one(new_user)
        return user_new
    
    async def get_user_by_id(self, id):
        user = await Users.find_one({"_id": id})
        return user

    async def get_user(self, user):
        userdb = await Users.find_one({"_id": user.id})
        if not userdb:
            userdb = await self.add_new_user(user)
            userdb = await Users.find_one({"_id": userdb.inserted_id})
        return userdb

    async def inc_reputation(self, from_user, to_user):
        if from_user["rep_limit"] > 0:
            await Users.update_one({"_id": from_user["_id"]}, {"$inc": {"rep_limit": -1, "rep_given": 1}})
            await Users.update_one({"_id": to_user["_id"]}, {"$inc": {"reputation": 1}})
            return True
        else:
            return False

    async def check_rep_goal(self, rep_count):
        congrats = await Goals.find_one({"goal": rep_count})
        if congrats:
            return congrats
        else:
            return False

    async def reset_rep_limits(self, limit):
        from_date = datetime.fromtimestamp((datetime.now().timestamp() - (60*60*24*7)))
        await Users.update_many({"$and": [{"custom_limit": {"$exists": False}}, {"createdAt": {"$lte": from_date}} ] }, {"$set": {"rep_limit": limit}})

    async def get_settings(self):
        settings = await Settings.find_one({})
        return settings

    async def is_admin(self, id):
        isAdmin = await Users.find_one({"_id": id, "admin": True})
        if isAdmin:
            return True
        else:
            return False

    async def get_congrats(self, page):
        congrats = Goals.find({}).sort("goal", 1).skip(page*6).limit(6)
        congrats_list = []
        async for grats in congrats:
            congrats_list.append(grats)
        return congrats_list

    async def add_new_congrats(self, congrats):
        congrat = congrats.__dict__
        new_congrats = await Goals.insert_one(congrat)
        return new_congrats
    
    async def get_single_congrats(self, goal):
        congrat = await Goals.find_one({"goal": goal})
        return congrat

    async def update_congrats_is_prize(self, goal, is_prize):
        await Goals.update_one({"goal": goal}, {"$set": {"is_prize": is_prize}})
    
    async def update_congrats_goal(self, goal, new_goal):
        await Goals.update_one({"goal": goal}, {"$set": {"goal": new_goal}})

    async def update_congrats_message(self, goal, message):
        await Goals.update_one({"goal": goal}, {"$set": {"message": message}})
    
    async def update_congrats_prize_name(self, goal, prize_name):
        await Goals.update_one({"goal": goal}, {"$set": {"prize_name": prize_name}})

    async def check_congrat_unique(self, goal):
        congrat = await Goals.find_one({"goal": goal})
        if congrat:
            return False
        else:
            return True
    
    async def set_rep_reset_limit(self, new_limit):
        await Settings.update_one({}, {"$set": {"rep_reset_limit": new_limit}})
    
    async def check_user_subscribed(self, user_id):
        try:
            for chat in TO_SUBSCRIBE:
                await bot.get_chat_member(chat, user_id)
                await sleep(0.2)
            subscribed = True
        except:
            subscribed = False
        return subscribed
    
    async def user_participating(self, user_id):
        participating = await Prizes.find_one({"$and": [{"status": "active"},{"participants": { "$in": [user_id]}}]})
        return participating
    
    async def user_participate(self, user_id):
        if await self.user_participating(user_id):
            return
        await Prizes.update_one({"status": "active"}, {"$push": {"participants": user_id}})
    
    async def check_pre_prize_draw(self, users):
        await Prizes.update_one({"status": "active"}, {"$set": {"participants": users}})
    
    async def get_all_participating_in_draw(self):
        participating = (await Prizes.find_one({"status": "active"}))['participants']
        return participating

    async def finish_prize_draw(self, legit_participants, prize, transaction, winner, status='finished'):
        await Prizes.update_one({"status": "active"}, {"$set": { "winner": winner, "transaction": transaction, "status": status, "legit_participants": legit_participants, "prize": prize, "end_date": datetime.now()}})
        await Prizes.insert_one(PrizeModel().__dict__)
    
    async def add_tron_wallet(self, id, wallet):
        await Users.update_one({"_id": id}, {"$set": {"address": wallet}})

    async def get_prizes(self):
        prizes = Goals.find({"is_prize": True}).sort("goal", 1)
        prize_list = []
        async for prize in prizes:
            prize_list.append(prize)
        return prize_list
    
    async def admin_get_stats(self):
        users = Users.aggregate([{ "$group": {
            "_id": 0,
            "user_count": {
                "$sum": 1
            },
            "total_rep_given": {
                "$sum": "$rep_given"
            },
            "max_rep": {
                "$max": "$reputation"
            }
        }}])
        result_users = []
        async for x in users:
            result_users.append(x)
        
        prizes = Prizes.aggregate([{"$match": {"status": "finished"}},{ "$group": {
            "_id": 0,
            "total_raffles": {
                "$sum": 1
            },
            "total_prize_sum": {
                "$sum": "$prize"
            }
        }}])
        result_prizes = []
        async for y in prizes:
            result_prizes.append(y)
        result = [result_users, result_prizes]
        return result

    async def update_prize(self, amount):
        await Settings.update_one({}, {"$set": {"prize": amount}})
    
    async def update_custom_limit(self, id, limit):
        await Users.update_one({"_id": id}, {"$set": {"custom_limit": limit}})

    async def reset_custom_limits(self):
        await Users.update_many({"custom_limit": {"$exists": True}}, [{"$set": {"rep_limit": "$custom_limit"}}])

    async def get_rep_top(self):
        top_reps = Users.find({}).sort("reputation", -1).limit(10)
        reps_list = []
        async for rep in top_reps:
            reps_list.append(rep)
        return reps_list