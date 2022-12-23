from starlette.config import Config

config = Config('../.config/bot/.conf')

DATABASE_POSTGRESS = config('DB_PSS_WISKET', cast=str)
TELEGRAM_API = config('TELEGRAM_API_WISKET', cast=str)
