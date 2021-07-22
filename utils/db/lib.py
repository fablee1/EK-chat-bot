from hashlib import sha256
from base58 import b58decode

def check_valid_tron_address(add):
    if not add[0] == "T":
        return False
    b58add = b58decode(add)
    h = sha256(sha256(b58add[:-4]).digest()).digest()
    if b58add[-4:] == h[:4]:
        return True
    return False

def to_number_emoji(num):
    emojis = ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
    result = ''
    for x in str(num):
        result += emojis[int(x)]
    return result
