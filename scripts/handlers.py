from imports.imports import dt
from imports.imports import ChoiseState
from imports.imports import Router, F, FSInputFile, ReplyKeyboardRemove

from imports.imports import Dispatcher, MemoryStorage, CommandStart, Message, FSMContext, CallbackQuery, CallbackData
from imports.imports import DialogCalendar, DialogCalendarCallback

from scripts.time_machine import News
from scripts.keyboards import make_row_keyboard, action_kb

from scripts.common_handlers import common_router

router = Router()

dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(router, common_router)  # Все хэндлеры бота находятся здесь


@dp.message(CommandStart())
async def dialog_timemachine(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=str("💨  Это — машина времени!  💨\n\n"
                 "Она может забросить тебя в новостной поток прошлого.\n\n"
                 "Доступны полёты в диапазоне\nс 28 августа 2000 по 31 мая 2021 года.\n\n"
                 "Выбери дату, пристегни ремни, ключ поверни и полетели! 🛸"),
        reply_markup=await DialogCalendar().start_calendar(2010)  # задаем год по умолчанию = среднему в датасете
    )
    await state.set_state(ChoiseState.choosing_date)


@dp.callback_query(DialogCalendarCallback.filter(), ChoiseState.choosing_date)
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    await state.set_data({})
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        if dt.datetime(2000, 8, 28) <= date <= dt.datetime(2021, 5, 31):
            await callback_query.message.answer('Ожидай: пересекаем новостное пространство 🚀')
            date_news = News(date)
            digest = date_news.get_category_digest()
            await state.update_data(date=date)
            await state.update_data(date_news=date_news)
            await callback_query.message.answer(
                digest, parse_mode='html')
            await (callback_query.message.answer
                   (text="Теперь можешь взглянуть на облако новостей этого дня, "
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


@router.message(ChoiseState.choosing_action, F.text.casefold() == "облако")
async def graph(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    data['date_news'].plot_categories()
    cat_distr_graph = FSInputFile("./graphs/cat_distr.png")
    await message.answer_photo(cat_distr_graph)


@router.message(ChoiseState.choosing_action, F.text.casefold() == "поиск")
async def invite_to_search(message: Message, state: FSMContext) -> None:
    await (message.answer
        (
        text="Набери произвольное описание темы или новости — того, что тебя интересуют, "
             "а я найду самую близкую по новость за эту дату.\n\n"
             "Примеры запросов: 'новости технологий', 'состояние экономики', 'результаты футбольных матчей",
        reply_markup=ReplyKeyboardRemove(),
    ))
    await state.set_state(ChoiseState.choosing_query)


@router.message(ChoiseState.choosing_action, F.text.casefold() == "выбрать другую дату")
async def invite_to_search(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_data({})
    await message.answer(
        text="Выбери дату в диапазоне с 28 августа 2000 года по 31 мая 2021 года",
        reply_markup=await DialogCalendar().start_calendar(2010),
    )
    await state.set_state(ChoiseState.choosing_date)


@router.message(ChoiseState.choosing_query)
async def search_similar_news(message: Message, state: FSMContext) -> None:
    q = message.text
    data = await state.get_data()
    best_news = data['date_news'].get_best_news(q)
    await message.answer(best_news, parse_mode='html')
    await message.answer(
        'Выбери дальнейший маршрут следования на нижней панели (ввод текста не сработает) 🔽',
        reply_markup=make_row_keyboard(action_kb)
    )
    await state.set_state(ChoiseState.choosing_action)
