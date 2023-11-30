from imports.imports import sys, asyncio, logging
from imports.imports import TOKEN, Bot
from scripts.handlers import dp

bot = Bot(token=TOKEN)


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
