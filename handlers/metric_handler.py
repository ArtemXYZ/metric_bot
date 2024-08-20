"""

"""

# -------------------------------- Стандартные модули
import asyncio
from pprint import PrettyPrinter as super_print
# -------------------------------- Сторонние библиотеки
from aiogram import types, Bot, Router, F
from aiogram.filters import CommandStart, Command, StateFilter, or_f
from aiogram.client.default import DefaultBotProperties  # Обработка текста HTML разметкой
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
# -------------------------------- Локальные модули

from handlers.states import *
from handlers.keyboard_generator import *
from db_connect.query_builder import *



# Назначаем роутер для всех типов чартов:
metric = Router()


# ----------------------------------------------------------------------------------------------------------------------
# Примет только кнопку старт
@metric.message(CommandStart())
async def start(message: types.Message, state: FSMContext, bot: Bot, session_jar: AsyncSession,
                session_gp_mart_sv: AsyncSession):  #

    # Получаем telegram_id из объекта message
    tg_id = message.from_user.id
    input_bot = bot

    # Удаляем сообщение с командой /start +
    if message.text == "/start":
        await message.delete()
    # ------------------------------------------------------------

    code_1c = await check_tg_id(tg_id, session_jar)

    # --------------------------------------------- 1
    if code_1c is None: # Опознание не прошло (отсутствует информация о пользователе в базе данных):

        await bot.send_message(f'<b>Пользователь не найден.\nПожалуйста зарегистрируйтесь через бот '
                               f'https://t.me/authorize_sv_bot</b>')

    # Если возникнет исключение в функции обращения к бд:
    elif code_1c == 'error':

        await bot.send_message(f'<b>Ошибка данных на сервере, обратитесь к администратору!</b>')
        #  todo - добавить кнопку.

    # --------------------------------------------- 2
    elif code_1c is not None and code_1c != 'error': # Опознание прошло успешно:

        code = code_1c[0]
        # щем по коду 1С данные на Грине:
        user_data = await get_user_data(code, session_gp_mart_sv)

        if user_data is None:

            print('Не удалось выполнить запрос к базе данных "gp_mart_sv" / забрать user_role, user_guid')
            await bot.send_message(f'<b>Ошибка данных на сервере, обратитесь к администратору!</b>')
            #  todo - добавить кнопку.

        elif user_data is not None:
            # Если функция вернула результат (не пусто), распакуем его:
            user_role, user_guid = user_data

            await state.set_state(UserStates.select_action)

            # await state.update_data(user_id=user_id, user_guid=user_guid, user_role=user_role) ?


            if user_role == 'Сотрудник' or user_role == 'Управляющий':
                if user_role == 'Сотрудник':
                    kb = get_keyboard('КПД', 'Оставить обратную связь', placeholder="Нажмите кнопку.",
                                      sizes=(2,))

                elif user_role == 'Управляющий':
                    kb = get_keyboard('КПД магазина', 'УГС магазина', placeholder="Нажмите кнопку.",
                                           sizes=(2,))

                await message.reply('Добро пожаловать! Выберите какой показатель вы хотите посмотреть:',
                                    reply_markup=kb)

            else:
                # АдмРРС или Не назначено
                await message.reply(
                    "Показатели в разработке, какой показатель вы бы хотели видеть тут? Подробно опишите в чате")
                await state.set_state(UserStates.feedback)


    # await state.clear()

# session_gp_mart_sv
# async def choose_action_handler(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     user_id = data.get('user_id')
#     user_guid = data.get('user_guid')
#     user_role = data.get('user_role')
#     kpd_message = None
#
#     if user_role in ['Сотрудник', 'Управляющий']:
#         if message.text == 'КПД':
#             if user_guid:
#                 kpd_message = await get_kpd_msg(user_guid)
#                 await message.reply(text=kpd_message)
#                 await save_bot_stat(user_id, 'КПД', kpd_message[:100])
#             else:
#                 await message.reply('Ошибка: не удалось получить данные о пользователе.')
#         elif message.text == 'Оставить обратную связь':
#             await message.reply('Какой показатель вы бы хотели видеть тут? Подробно опишите в чате')
#             await state.set_state(UserStates.feedback)
#         else:
#             await message.reply('Неверный выбор. Попробуйте снова.')
#             await save_bot_stat(user_id, message.text, 'Неверный выбор. Попробуйте снова.')
#     else:
#         # АдмРРС или Не назначено
#         await message.reply("Описание, что вы хотели бы видеть в разделе показателей:")
#         await state.set_state(UserStates.feedback)





