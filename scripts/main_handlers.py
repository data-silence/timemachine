from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, FSInputFile

from scripts.processors import make_row_keyboard
# from app import keyboard_action
from scripts.processors import action_kb

router = Router()


class ChoiseState(StatesGroup):
    choosing_date = State()
    choosing_action = State()
    choosing_query = State()


@router.message(ChoiseState.choosing_action, F.text.casefold() == "график")
async def graph(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    data['date_news'].plot_categories()
    cat_distr_graph = FSInputFile("./graphs/cat_distr.png")
    await message.answer_photo(cat_distr_graph)
    await state.set_state(ChoiseState.choosing_action)


@router.message(ChoiseState.choosing_action, F.text.casefold() == "поиск")
async def invite_to_search(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Введи описание темы или новости, что тебя интересуют, "
             "а я подберу самое близкое по смыслу из собранных на дату новостей.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(ChoiseState.choosing_query)


@router.message(ChoiseState.choosing_query)
async def search_similar_news(message: Message, state: FSMContext) -> None:
    q = message.text
    data = await state.get_data()
    best_news = data['date_news'].get_best_news(q)
    await message.answer(best_news, parse_mode='html', reply_markup=make_row_keyboard(action_kb))
    await state.set_state(ChoiseState.choosing_action)
