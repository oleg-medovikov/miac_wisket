from starlette.config import Config

config = Config('../.config/bot/.conf')

DATABASE_POSTGRESS = config('DB_PSS_WISKET', cast=str)
DATABASE_SVUP = config('DATABASE_SVUP', cast=str)
TELEGRAM_API = config('TELEGRAM_API_WISKET', cast=str)
