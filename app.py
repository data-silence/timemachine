from imports.imports import TOKEN, sys, asyncio, dt, logging
from scripts.processors import validate_user_date
from scripts.time_machine import News
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile, KeyboardButton, CallbackQuery, ReplyKeyboardMarkup, Message
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_calendar import DialogCalendar, DialogCalendarCallback
from aiogram.filters import CommandStart

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# initialising keyboard, each button will be used to start a calendar with different initial settings
kb = [
    [KeyboardButton(text='Dialog Calendar w year')]
]
start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


@dp.message(CommandStart())
async def dialog_cal_handler_year(message: Message):
    await message.answer(
        text="Это машина времени, и она может забросить тебя в новостной поток прошлого.\n"
             "Доступны полёты в диапазоне с 28 августа 2000 года по 31 мая 2021 года.\n"
             "Выбери дату и поехали!",
        reply_markup=await DialogCalendar().start_calendar(2000)
    )


# dialog calendar usage
@dp.callback_query(DialogCalendarCallback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer('Летим в прошлое и собираем новости. Ожидайте...')
        news = News(date)
        digest = news.get_category_digest()
        await callback_query.message.answer(
            digest, parse_mode='html')

#
# async def get_date(user_date):
#         news = News(user_date)
#         digest = news.get_category_digest()
#         news.plot_categories()
#         cat_distr_graph = FSInputFile("./graphs/cat_distr.png")
#     else:
#         digest = 'Введите дату'
#     # await message.answer(digest, parse_mode='html')
#     await message.answer_photo(cat_distr_graph)



# @dp.message()
# async def get_date(message: types.Message):
#     user_date = validate_user_date(message.text)
#     if isinstance(user_date, dt.date):
#         news = News(user_date)
#         digest = news.get_category_digest()
#         news.plot_categories()
#         cat_distr_graph = FSInputFile("./graphs/cat_distr.png")
#     else:
#         digest = 'Введите дату'
#     # await message.answer(digest, parse_mode='html')
#     await message.answer_photo(cat_distr_graph)


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
