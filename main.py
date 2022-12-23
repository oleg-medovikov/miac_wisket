import warnings
import asyncio

from disp import dp, on_startup
from shed import scheduler

warnings.filterwarnings("ignore")


async def main():
    await asyncio.gather(
        on_startup(dp),
        scheduler(),
        )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
