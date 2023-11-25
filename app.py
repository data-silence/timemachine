from imports.imports import TOKEN, sys, asyncio, dt, logging
from scripts.processors import validate_user_date
from scripts.time_machine import News
from aiogram import Bot, Dispatcher, types

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def get_date(message: types.Message):
    user_date = validate_user_date(message.text)
    if isinstance(user_date, dt.date):
        news = News(user_date)
        digest = news.get_category_digest()
    else:
        digest = 'Введите дату'
    await message.answer(digest, parse_mode='html')
    # await  message.answer(news.plot_categories())


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
