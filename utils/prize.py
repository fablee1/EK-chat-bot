from asyncio import sleep
from handlers.users.keyboards import chat_prize_trans
from utils.db.database import DBCommands
from tronpy import Tron
from tronpy.keys import PrivateKey
from data.config import MAIN_CHAT_ID, TRON_PRIV_KEY, TRON_ADD, TRON_USDT_CONTRACT_ADD
from load_all import bot
from random import random
from math import floor

db = DBCommands()

priv_key = PrivateKey(bytes.fromhex(TRON_PRIV_KEY))

async def transfer_prize(add, amount):
    client = Tron()
    contract = client.get_contract(TRON_USDT_CONTRACT_ADD)
    txb = (
        contract.functions.transfer(add, int(floor(amount*1000000)))
        .with_owner(TRON_ADD)
        .fee_limit(20_000_000)
        .build()
        .sign(priv_key)
    )
    result = txb.broadcast().wait()
    return result

async def get_add_bals(add):
    client = Tron()
    contract = client.get_contract("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
    trx_bal = round(client.get_account_balance(add), 0)
    usdt_bal = round(contract.functions.balanceOf(add) / 10 ** 6, 2)
    return [trx_bal, usdt_bal]
    

async def check_all_subscribed(participants):
    legit_participants = []
    for participant in participants:
        try:
            info = await bot.get_chat_member(MAIN_CHAT_ID, participant)
            if not info['status'] == 'left':
                legit_participants.append(participant)
        except:
            pass
        await sleep(0.1)
    await db.check_pre_prize_draw(legit_participants)
    return legit_participants

async def get_random_person(participants):
    rand_person = floor(random() * len(participants))
    id = participants[rand_person]
    user = await db.get_user_by_id(id)
    return user

async def send_chat_prize_msg(winner, trans=None, participant_count=0):
    msg = ("Розыгрыш закончен!\n\n"
            f"Участвовало - {participant_count}\n"
            f"Поздравляем победителя - @{winner['username']}!\n\n"
            "Проверь свой кошелёк 💰"
    )

    await bot.send_message(MAIN_CHAT_ID, msg, reply_markup=await chat_prize_trans(trans))

async def start_airdrop():
    all_participants = await db.get_all_participating_in_draw()
    legit_participants = await check_all_subscribed(all_participants)

    transaction_id = None
    winner = None

    if len(legit_participants) > 0:
        user = await get_random_person(legit_participants)
        winner = user
        prize = (await db.get_settings())['prize']
        result = await transfer_prize(user['address'], prize)
        transaction_id = result['id']
        await send_chat_prize_msg(user, transaction_id, participant_count=len(legit_participants))
        await db.finish_prize_draw(legit_participants, prize, transaction_id, winner)