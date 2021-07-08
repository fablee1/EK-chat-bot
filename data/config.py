from environs import Env

env = Env()
env.read_env()
from pathlib import Path


BOT_MODE = env.str("BOT_MODE")

TOKEN = env.str("TOKEN")
admin_id = env.int("ADMIN_ID")
db_user = env.str("DB_USER")
db_pass = env.str("DB_PASS")
host = env.str("HOST", None)
database = env.str("DB_NAME")

HEROKU_APP_NAME = env.str('HEROKU_APP_NAME', None)

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = env.int('PORT', None)

I18N_DOMAIN = 'ekchatbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'