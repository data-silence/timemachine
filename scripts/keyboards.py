from imports.imports import ReplyKeyboardMarkup, KeyboardButton

kb = [
    [KeyboardButton(text='Календарь')]
]
start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
action_kb = ["График", "Поиск"]


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Creates a replay keyboard with buttons in a single row
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row_1 = [KeyboardButton(text=item) for item in items]
    row_2 = [KeyboardButton(text='Выбрать другую дату')]
    row = [row_1, row_2]
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True, input_field_placeholder="Что делаем дальше?")
