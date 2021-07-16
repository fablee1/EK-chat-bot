import asyncio
from utils.db.database import DBCommands
from tronpy import Tron
from tronpy.keys import PrivateKey
from data.config import MAIN_CHAT, TRON_PRIV_KEY, TRON_ADD, TRON_USDT_CONTRACT_ADD
from load_all import bot
from random import random
from math import floor

db = DBCommands()

priv_key = PrivateKey(bytes.fromhex(TRON_PRIV_KEY))

async def transfer_prize(add, amount):
    client = Tron()
    contract = client.get_contract(TRON_USDT_CONTRACT_ADD)
    txb = (
        contract.functions.transfer(add, amount*1000000)
        .with_owner(TRON_ADD)
        .fee_limit(20_000_000)
        .build()
        .sign(priv_key)
    )
    result = txb.broadcast().wait()
    return result

async def check_all_subscribed(participants):
    legit_participants = []
    for participant in participants:
        try:
            info = await bot.get_chat_member(MAIN_CHAT, participant)
            if not info['status'] == 'left':
                legit_participants.append(participant)
        except:
            pass
        await asyncio.sleep(0.1)
    await db.check_pre_prize_draw(legit_participants)
    return legit_participants

async def start_airdrop():
    all_participants = await db.get_all_participating_in_draw()
    legit_participants = await check_all_subscribed(all_participants)

    # If no legit participants do nothing
    if len(legit_participants) == 0:
        # return await bot.send_message(564143733, "Нет участников.")
        return

    # Choose random person
    rand_person = floor(random() * len(legit_participants))
    id = legit_participants[rand_person]
    user_wallet = await db.get_user_by_id(id)
    prize = (await db.get_settings())['prize']

    # Send prize
    # result = await transfer_prize(user_wallet['address'], prize)
    await db.finish_prize_draw(legit_participants, prize)
    # await bot.send_message(id, result)

