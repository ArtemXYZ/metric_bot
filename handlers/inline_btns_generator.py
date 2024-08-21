from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Функция для генерации инлайн-кнопок;
def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (2,)):

    """
    sizes: кортеж с числами, определяющими размеры строк.
    По умолчанию это (2,), что означает две кнопки в одной строке.
    *,  # - запрет на передачу не именнованных аргументов

    Метод adjust принимает кортеж sizes и настраивает кнопки по строкам в соответствии с указанными размерами.
    Если количество кнопок превышает сумму всех значений в sizes, то:

    Если параметр repeat=True, то размеры из кортежа будут циклически повторяться до тех пор,
    пока не будут размещены все кнопки.
    Если repeat=False (или этот параметр не указан), то оставшиеся кнопки будут сгруппированы в строку по размеру
    последнего элемента в sizes.
    """

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        # dict_items([('one', 1), ('two', 2), ('three', 3), ('four', 4)]) - пример вида
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()

