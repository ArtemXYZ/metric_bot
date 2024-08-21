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
from handlers.keyboard_generator import *  # Клавиатура
from handlers.inline_btns_generator import *  # Инлайн кнопки
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

    # Удаляем сообщение с командой /start +
    if message.text == "/start":
        await message.delete()
    # ------------------------------------------------------------

    code_1c = await check_tg_id(tg_id, session_jar)

    # --------------------------------------------- 1
    if code_1c is None: # Опознание не прошло (отсутствует информация о пользователе в базе данных):

        await bot.send_message(chat_id=tg_id, text=f'<b>Пользователь не найден.\nПожалуйста зарегистрируйтесь через бот'
                               f' https://t.me/authorize_sv_bot</b>')

    # Если возникнет исключение в функции обращения к бд:
    elif code_1c == 'error':

        await bot.send_message(chat_id=tg_id, text=f'<b>Ошибка данных на сервере, обратитесь к администратору!</b>')
        #  todo - добавить кнопку.



    # --------------------------------------------- 2
    elif code_1c is not None and code_1c != 'error': # Опознание прошло успешно:

        code = code_1c[0]
        # print(f'"code_1c": {code}')

        # щем по коду 1С данные на Грине:
        user_data = await get_user_data(code, session_gp_mart_sv)
        # print(f'"user_data": {user_data}')

        if user_data is None:

            print('Не удалось выполнить запрос к базе данных "gp_mart_sv" / забрать user_role, user_guid')
            await bot.send_message(chat_id=tg_id, text=f'<b>Ошибка данных на сервере, обратитесь к администратору!</b>')
            #  todo - добавить кнопку.

        elif user_data is not None:
            # Если функция вернула результат (не пусто), распакуем его:
            user_role, user_guid = user_data
            # print(f'"user_role": {user_role}, "user_guid": {user_guid}')

            await state.set_state(UserStates.select_action)
            await state.update_data(user_id=code, user_guid=user_guid, user_role=user_role)


            if user_role == 'Сотрудник' or user_role == 'Управляющий':
                if user_role == 'Сотрудник':
                    kb = get_keyboard('КПД', 'Оставить обратную связь', placeholder="Нажмите кнопку.",
                                      sizes=(2,))

                elif user_role == 'Управляющий':
                    kb = get_keyboard('КПД магазина', 'УГС магазина', placeholder="Нажмите кнопку.",
                                           sizes=(2,))

                # await message.reply('Добро пожаловать! Выберите какой показатель вы хотите посмотреть:',
                #                     reply_markup=kb)
                await bot.send_message(chat_id=tg_id,
                                       text=f'Добро пожаловать! Выберите какой показатель вы хотите посмотреть:',
                                       reply_markup=kb)

            else:
                # АдмРРС или Не назначено
                # await message.reply(
                #     "Показатели в разработке, какой показатель вы бы хотели видеть тут? Подробно опишите в чате")

                await bot.send_message(chat_id=tg_id, text=f'Показатели в разработке, какой показатель '
                                                           f'вы бы хотели видеть тут? Подробно опишите в чате')

                await state.set_state(UserStates.feedback)




# session_gp_mart_sv
@metric.message(StateFilter(UserStates.select_action)) # , F.text
async def choose_action_handler(message: types.Message, state: FSMContext, session_jar: AsyncSession):
    # F.data in ('КПД', 'КПД магазина', 'Оставить обратную связь', 'УГС магазина')

    # -----------------------------
    data = await state.get_data()
    user_id = data.get('user_id')
    user_guid = data.get('user_guid')
    user_role = data.get('user_role')

    # тоговое сообщение с расчетами:
    # kpd_message = await get_kpd_msg(user_guid, session_jar) - тест - пока не работает.
    # -----------------------------

    # ------------------------------------- 1
    if user_role in ['Сотрудник']:

        if message.text == 'КПД':

                await message.reply(
                    'Сообщение с инлайн-кнопками.',
                    reply_markup=get_callback_btns(btns={
                        'КНОПКА 1': 'btns1', 'КНОПКА 2': 'btns2', 'КНОПКА 3': 'btns3'}, sizes=(3,)))  # sizes=(2, 1,)))


        elif message.text == 'Оставить обратную связь':

            await message.reply('Какой показатель вы бы хотели видеть тут? Подробно опишите в чате')
            await state.set_state(UserStates.feedback)



    # ------------------------------------- 2
    elif user_role in ['Управляющий']:

        if message.text == 'КПД магазина':

            await message.reply(
                'Сообщение с инлайн-кнопками.',
                reply_markup=get_callback_btns(btns={
                    'КНОПКА 1': 'btns1', 'КНОПКА 2': 'btns2', 'КНОПКА 3': 'btns3'}, sizes=(3,)))



        elif message.text == 'УГС магазина':

            await message.reply(
                'Сообщение с инлайн-кнопками.',
                reply_markup=get_callback_btns(btns={
                    'КНОПКА 1': 'btns1', 'КНОПКА 2': 'btns2', 'КНОПКА 3': 'btns3'}, sizes=(3,)))


    # ------------------------------------- 3
    else:
        # АдмРРС или Не назначено
        await message.reply("Описание, что вы хотели бы видеть в разделе показателей:")
        await state.set_state(UserStates.feedback)



@metric.message(StateFilter(UserStates.feedback))
async def feedback_handler(message: types.Message, state: FSMContext, session_jar: AsyncSession):
    data = await state.get_data()
    user_id = data.get('user_id')

    await save_bot_stat(user_id, "Обратная связь", message.text, session_jar)


    await message.reply("Ваше сообщение отправлено разработчикам. "
                        "Спасибо за обратную связь! Можете продолжать давать обратную связь или нажмите "
                        "/start для перезапуска бота"
                        )
    # await state.clear()  # сли надо то чистим в текущей логике не надо.




# ---------------------------------- реагируем на инлайн кнопки:

@metric.callback_query(F.data.startswith('btns1'))  # - меняем келбек под соотв. кнопку
async def get_ask(callback: types.CallbackQuery, state: FSMContext, bot: Bot):

    await callback.answer()  # Ответ на сервер что кнопку нажали.

    # Получаем telegram_id из объекта message
    tg_id = callback.from_user.id

    # аменяем сообщение с кнопками
    await callback.message.edit_text(
        text=f'<b>Вы перешли в раздел ... .</b>\n'
             f'\n'            
             f'Опишите суть своего обращения (проблемы) и '
             f'бот направит заявку на ответственных специолистов в части касающейся.'
    )

    # Отправляем новое сообщение
    # await bot.send_message(chat_id=tg_id, text=f'Ответ на нажатие кнопки')