from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from scripts.processors import make_row_keyboard

keyboard_action = ["Распределение новостей", "Похожая новость"]

router = Router()

class ChoiseState(StatesGroup):
    choosing_action = State()


