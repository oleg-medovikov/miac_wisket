from os import getenv
from dataclasses import dataclass
from dotenv import main

main.load_dotenv(".conf")


@dataclass
class Settings:
    BOT_API: str
    PSQL: str


settings = Settings(
    BOT_API=getenv("BOT_API", default=""),
    PSQL=getenv("PSQL", default=""),
)
