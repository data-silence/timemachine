from aiogram import F, Router
from aiogram.filters import Command
# from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from scripts.keyboards import make_row_keyboard, action_kb
from scripts.handlers import ChoiseState
from aiogram_calendar import DialogCalendar

router = Router()


# @router.message(StateFilter(None), Command(commands=["cancel"]))
# @router.message(default_state, F.text.lower() == "отмена")
# async def cmd_cancel_no_state(message: Message, state: FSMContext):
#     # Стейт сбрасывать не нужно, удалим только данные
#     await state.set_data({})
#     await message.answer(
#         text="Нечего отменять",
#         reply_markup=ReplyKeyboardRemove()
#     )

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_data({})
    await state.clear()
    await message.answer(
        text=str("💨  Это — машина времени!  💨\n\n"
                 "Она может забросить тебя в новостной поток прошлого.\n\n"
                 "Доступны полёты в диапазоне с 28 августа 2000 года по 31 мая 2021 года.\n\n"
                 "Выбери дату, пристегни ремни, ключ поверни и полетели! 🛸"),
        reply_markup=await DialogCalendar().start_calendar(2010)
    )
    await state.set_state(ChoiseState.choosing_date)




@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await state.set_data({})
    await message.answer(
        text="Снова готовы к старту",
        reply_markup=await DialogCalendar().start_calendar(2010)
    )
    await state.set_state(ChoiseState.choosing_date)
