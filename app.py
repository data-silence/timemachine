from imports.imports import TOKEN, sys, asyncio, logging, dt
from scripts.time_machine import News
from scripts.keyboards import make_row_keyboard, action_kb
from scripts.handlers import ChoiseState

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_calendar import DialogCalendar, DialogCalendarCallback
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData

from scripts.handlers import router
from scripts import common_handlers

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(router, common_handlers.router)  # Все хэндлеры бота находятся здесь


@dp.message(CommandStart())
async def dialog_timemachine(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=str("💨  Это — машина времени!  💨\n\n"
                 "Она может забросить тебя в новостной поток прошлого.\n\n"
                 "Доступны полёты в диапазоне\nс 28 августа 2000 по 31 мая 2021 года.\n\n"
                 "Выбери дату, пристегни ремни, ключ поверни и полетели! 🛸"),
        reply_markup=await DialogCalendar().start_calendar(2010)
    )
    await state.set_state(ChoiseState.choosing_date)


@dp.callback_query(DialogCalendarCallback.filter(), ChoiseState.choosing_date)
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    await state.set_data({})
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        # await callback_query.message.answer('Идёт проверка правильности введенных координат')
        if dt.datetime(2000, 8, 28) <= date <= dt.datetime(2021, 5, 31):
            await callback_query.message.answer('Ожидай: пересекаем новостное пространство 🚀')
            date_news = News(date)
            digest = date_news.get_category_digest()
            await state.update_data(date=date)
            await state.update_data(date_news=date_news)
            await callback_query.message.answer(
                digest, parse_mode='html')
            await (callback_query.message.answer
                   (text="Теперь можешь взглянуть на график распределения категорий новостей этого дня, "
                         "или попробовать найти самую близкую новость на интересующую тебя тему в тот день.\n\n"
                         "Выбери дальнейший маршрут следования на нижней панели 🔽",
                    reply_markup=make_row_keyboard(action_kb)
                    ))
            await state.set_state(ChoiseState.choosing_action)
        else:
            await (callback_query.message.answer
                   (text="Знаем о новостях за период с 28 августа 2000 года по 31 мая 2021, "
                         "до остальных долететь пока не можем. Попробуй ещё разок, пожалуйста",
                    reply_markup=await DialogCalendar().start_calendar(2010)
                    ))


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
