from environs import Env

env = Env()
env.read_env()
from pathlib import Path


BOT_MODE = env.str("BOT_MODE", None)

MAIN_CHAT_ID = -1001320961407
TO_SUBSCRIBE = [-1001320961407]

TOKEN = env.str("TOKEN")
DB_CONN = env.str("DB_CONN")
HEROKU_APP_NAME = env.str('HEROKU_APP_NAME', None)

TRON_PRIV_KEY = env.str('TRON_PRIV_KEY')
TRON_ADD = env.str('TRON_ADD')
TRON_USDT_CONTRACT_ADD = env.str('TRON_USDT_CONTRACT_ADD')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
# WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
# WEBHOOK_PATH = ""
# WEBHOOK_URL = "https://acab39fc7135.ngrok.io"

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = env.int('PORT', None)
# WEBAPP_HOST = "127.0.0.1"
# WEBAPP_PORT = 5000

I18N_DOMAIN = 'ekchatbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'