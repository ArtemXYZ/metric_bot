"""
Модуль содержит функции асинхронных SQL запросов к базам данных.
В основном с помощью ОРМ.
"""
# check_telegram_id
# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------- Импорт стандартных библиотек Пайтона
# ---------------------------------- Импорт сторонних библиотек
from sqlalchemy import text
# from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
# -------------------------------- Локальные модули
# from sql.get_user_data_sql import *
# from working_databases.async_engine import *

from db_connect.async_engine import *

from sql.all_sql import * # Доступ к файлу где хранятся все запросы

# ----------------------------------------------------------------------------------------------------------------------

async def check_tg_id(tg_id, session:AsyncSession):

    """
    Функция для опознания пользователя. На вход поступает сессия (готовое подключение к бд) и телеграмм айди.
    Далее, осуществляется запрос.
    sql = get_tg_id_jar
    Вернет: code as user_id
    """
    try:
        # Форматируем SQL запрос, если есть аргументы для форматирования
        formatted_query = get_tg_id_jar.format(tg_id) #

        # Извлекаем данные:
        result_tmp = await session.execute(text(formatted_query))
        results = result_tmp.one_or_none()  # Возвращает одну строку или None
        return results
    except Exception as error_text:
        print(f'Ошибка в "check_tg_id": {error_text}')
        return None

async def get_user_data(tg_id, session: AsyncSession):
    """
        Функция для извлечения данных пользователя. На вход поступает сессия (готовое подключение к бд) и \
        телеграмм айди.  Далее, осуществляется запрос.
        sql = get_user_data_gp_mart_sv
        Вернет:
    """
    try:
        formatted_query = get_user_data_gp_mart_sv.format(tg_id)  #
        # Извлекаем данные:
        result_tmp = await session.execute(text(formatted_query))
        results = result_tmp.fetchone()  # Возвращает одну строку результата в виде кортежа или None
        return results
    except Exception as error_text:
        print(f'Ошибка в "get_user_data": {error_text}')
        return 'error'








    # # Открываем контекстный менеджер для сохранения данных.
    #     async with session_pool() as pool:
    #         # Только действующие сотрудники:
    #         # Либо ноль либо фелсе:
    #         query = select(Users.id_tg).where(or_(Users.is_deleted == False, Users.is_deleted == 0))
    #         # В SQLAlchemy условие выборки должно быть записано без использования Python-оператора not.
    #
    #         result_tmp = await pool.execute(query)
    #         results = result_tmp.scalars().all()  #






