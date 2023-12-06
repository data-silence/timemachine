from imports.imports import Router, Command, F, Message, FSMContext
from imports.imports import DialogCalendar
from imports.imports import help_text, donate_text

from scripts.handlers import ChoiseState

common_router = Router()


@common_router.message(Command(commands=["start"]))
@common_router.message(F.text.lower() == "старт")
async def start_handler(message: Message, state: FSMContext) -> None:
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


@common_router.message(Command(commands=["cancel"]))
@common_router.message(F.text.lower() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_data({})
    await message.answer(
        text="Снова готовы к старту двигателей",
        reply_markup=await DialogCalendar().start_calendar(2010)
    )
    await state.set_state(ChoiseState.choosing_date)


@common_router.message(Command(commands=["help"]))
@common_router.message(F.text.lower() == "помощь")
async def help_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=help_text,
        reply_markup=await DialogCalendar().start_calendar(2010)
    )
    await state.set_state(ChoiseState.choosing_date)


@common_router.message(Command(commands=["donate"]))
async def donate_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=donate_text,
        reply_markup=await DialogCalendar().start_calendar(2010)
    )
    await state.set_state(ChoiseState.choosing_date)
