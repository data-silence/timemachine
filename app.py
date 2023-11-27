from aiogram.fsm import state

from imports.imports import TOKEN, sys, asyncio, dt, logging
# from scripts.processors import validate_user_date
from scripts.time_machine import News
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile, KeyboardButton, CallbackQuery, ReplyKeyboardMarkup, Message
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_calendar import DialogCalendar, DialogCalendarCallback
from aiogram.filters import CommandStart
from aiogram.filters import Command, StateFilter
from scripts.main_handlers import ChoiseState

from scripts import common_handlers, main_handlers
from scripts.processors import make_row_keyboard, action_kb

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(common_handlers.router, main_handlers.router)


@dp.message(CommandStart())
async def dialog_cal_handler_year(message: Message, state: FSMContext):
    await message.answer(
        text="Это машина времени, и она может забросить тебя в новостной поток прошлого.\n"
             "Доступны полёты в диапазоне с 28 августа 2000 года по 31 мая 2021 года.\n"
             "Выбери дату и поехали!",
        reply_markup=await DialogCalendar().start_calendar(2010)
    )
    await state.set_state(ChoiseState.choosing_date)


# dialog calendar usage
@dp.callback_query(DialogCalendarCallback.filter(), ChoiseState.choosing_date)
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer('Пристегните ремни и ожидайте: летим в прошлое за новостями...')
        date_news = News(date)
        digest = date_news.get_category_digest()
        await state.update_data(date=date)
        await state.update_data(date_news=date_news)
        # data = await state.get_data()
        # data['date'] = date
        # data['date_news'] = News(date)
        # digest = data['date_news'].get_category_digest()
        await callback_query.message.answer(
            digest, parse_mode='html')
        await callback_query.message.answer(
            text="Теперь вы можете посмотреть на график распределения категорий новостей дня, "
                 "или попробовать найти самую близкую новость на интересующую вас тему за эту дату",
            reply_markup=make_row_keyboard(action_kb)
        )
        await state.set_state(ChoiseState.choosing_action)


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
