from utils.db.database import DBCommands
from tronpy import AsyncTron
from tronpy.keys import PrivateKey
from data.config import TRON_PRIV_KEY, TRON_ADD, TRON_USDT_CONTRACT_ADD

db = DBCommands()

priv_key = PrivateKey(bytes.fromhex(TRON_PRIV_KEY))

async def transfer_prize(add):
    async with AsyncTron() as client:
        contract = client.get_contract(TRON_USDT_CONTRACT_ADD)
        amount = await db.get_settings()
        txb = (
            contract.functions.transfer(add, amount.get('prize'))
            .with_owner(TRON_ADD)
            .fee_limit(20_000_000)
        )
        txn = await txb.build()
        txn_ret = await txn.sign(priv_key).broadcast()
        result = await txn_ret.wait()
        return result