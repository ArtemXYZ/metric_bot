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
        formatted_query = tg_id_jar.format(tg_id) #

        # Извлекаем данные:
        result_tmp = await session.execute(text(formatted_query))
        results = result_tmp.one_or_none()  # Возвращает одну строку или None
        return results
    except Exception as error_text:
        print(f'Ошибка в "check_tg_id": {error_text}')
        return 'error'


async def get_user_data(tg_id, session: AsyncSession):
    """
        Функция для извлечения данных пользователя. На вход поступает сессия (готовое подключение к бд) и \
        телеграмм айди.  Далее, осуществляется запрос.
        sql = get_user_data_gp_mart_sv
        Вернет: ('235UI',)
    """
    try:
        formatted_query = user_data_gp_mart_sv.format(tg_id)  #
        result_tmp = await session.execute(text(formatted_query)) # Извлекаем данные:
        results = result_tmp.fetchone()  # Возвращает одну строку результата в виде кортежа или None
        # await session.dispose()  # Закрытие соединения вручную. Важно! Если не закрыть соединение,\
        # будут ошибки!
        return results
    except Exception as error_text:
        print(f'Ошибка в результате запроса в функции "get_user_data": {error_text}')
        return None


# ----------------------------- KPD --------------------------------
async def get_kpd_user(user_guid, session: AsyncSession):
    """
        Функция для извлечения данных о КПД пользователя. На вход поступает сессия (готовое подключение к бд, Джарвис)\
        и гуид.
        sql = get_kpd_user
        Вернет:
    """

    try:
        formatted_query = kpd_user.format(user_guid)  #
        result_tmp = await session.execute(text(formatted_query)) # Извлекаем данные:
        results = result_tmp.fetchone()  # Возвращает одну строку или None
        return results
    except Exception as error_text:
        print(f'Ошибка в результате запроса в функции "get_kpd_user": {error_text}')
        return None


# async def get_kpd_rating(user_guid, session: AsyncSession):
#     """
#         Функция для извлечения данных о рейтинге пользователя. На вход поступает сессия \
#         (готовое подключение к бд, Джарвис) и гуид.
#         sql = get_kpd_user
#         Вернет:
#     """
#
#     try:
#         formatted_query = get_kpd_rating.format(user_guid)  #
#         result_tmp = await session.execute(text(formatted_query)) # Извлекаем данные:
#         results = result_tmp.fetchone()  # Возвращает одну строку или None
#         return results
#     except Exception as error_text:
#         print(f'Ошибка в "get_user_data": {error_text}')
#         return None


async def get_kpd_rating_user(user_guid, session: AsyncSession):
    """
        Функция для извлечения рейтинга КПД пользователя в текущем месяце. На вход поступает сессия \
        (готовое подключение к бд, Джарвис) и гуид.
        sql = get_kpd_rating_user
        Вернет:
    """

    try:
        formatted_query = kpd_rating_user.format(user_guid)  #
        result_tmp = await session.execute(text(formatted_query)) # Извлекаем данные:
        results = result_tmp.fetchone()  # Возвращает одну строку или None (картеж) (1, 'Alice')
        return results
    except Exception as error_text:
        print(f'Ошибка в результате запроса в функции "get_kpd_rating_user": {error_text}')
        return None


async def get_top5_kpd_rating_users(user_guid, session: AsyncSession):
    """
        Функция для извлечения Топ 5 пользователей по рейтингу в текущем месяце. На вход поступает сессия \
        (готовое подключение к бд, Джарвис) и гуид.
        sql = get_top5_kpd_rating_users
        Вернет: массив: UserName, kpd, rating_kpd
    """

    try:
        formatted_query = top5_kpd_rating_users.format(user_guid)  #
        result_tmp = await session.execute(text(formatted_query)) # Извлекаем данные:
        results = result_tmp.fetchall()  # Возвращает список кортежей: [(1, 'Alice'), (2, 'Bob')]
        return results
    except Exception as error_text:
        print(f'Ошибка в результате запроса в функции "get_top5_kpd_rating_users": {error_text}')
        return None



async def get_top5end_kpd_rating_users(user_guid, session: AsyncSession):
    """
        Функция для извлечения Топ 5 пользователей по рейтингу в текущем месяце. На вход поступает сессия \
        (готовое подключение к бд, Джарвис) и гуид.
        sql = get_top5_kpd_rating_users
        Вернет: массив: UserName, kpd, rating_kpd
    """

    try:
        formatted_query = top5end_kpd_rating_users.format(user_guid)  #
        result_tmp = await session.execute(text(formatted_query)) # Извлекаем данные:
        results = result_tmp.fetchall()  # Возвращает список кортежей: [(1, 'Alice'), (2, 'Bob')]
        return results
    except Exception as error_text:
        print(f'Ошибка в результате запроса в функции "get_top5end_kpd_rating_users": {error_text}')
        return None






# async def get_kpd_dinamic(user_guid, session: AsyncSession):
#     """
#         Функция для извлечения данных о рейтинге пользователя. На вход поступает сессия \
#         (готовое подключение к бд, Джарвис) и гуид.
#         sql = get_kpd_user
#         Вернет:
#     """
#
#     try:
#         formatted_query = get_kpd_rating.format(user_guid)  #
#         result_tmp = await session.execute(text(formatted_query)) # Извлекаем данные:
#         results = result_tmp.fetchone()  # Возвращает одну строку или None
#         return results
#     except Exception as error_text:
#         print(f'Ошибка в "get_user_data": {error_text}')
#         return None











# ---------------------------------------- Итог, сборка общих показателей рейтинга КПД:
async def get_kpd_msg(user_guid, session: AsyncSession):
    """
        Функция для формирования данных о рейтинге КПД и др. данных. На вход поступает гуид.
        Основная информация извлекается вложенными функциями.

        Вернет: текст с показателями.
    """
    # try:

    # 0. КПД пользователя:
    kpd = await get_kpd_user(user_guid, session)
    print(f'get_kpd_user: {kpd}')

    # 1. Рейтинг конкретного пользователя в текущем месяце (картеж или None):
    kpd_rating_user = await get_kpd_rating_user(user_guid, session)
    print(f'kpd_rating_user: {kpd_rating_user}')

    # 2. Топ 5 пользователей по рейтингу в текущем месяце (картеж или None):
    top5_kpd_rating_users = await get_top5_kpd_rating_users(user_guid, session)
    print(f'top5_kpd_rating_users: {top5_kpd_rating_users}')

    # 3. Топ 5 пользователей худших по рейтингу (5 нижних позиций) в текущем месяце (картеж или None):
    top5end_kpd_rating_users = await get_top5end_kpd_rating_users(user_guid, session)
    print(f'top5end_kpd_rating_users: {top5end_kpd_rating_users}')


    # rating_kpd = await get_kpd_rating(user_guid)
    # print(f'get_kpd_rating": {rating_kpd}')


    # kpd_dinamic = await get_kpd_dinamic(user_guid)
    # print(f'kpd_dinamic: {kpd_dinamic}')









        # return results
    # except Exception as error_text:
    #     print(f'Ошибка в "get_user_data": {error_text}')
    #     return 'error'





    # # Открываем контекстный менеджер для сохранения данных.
    #     async with session_pool() as pool:
    #         # Только действующие сотрудники:
    #         # Либо ноль либо фелсе:
    #         query = select(Users.id_tg).where(or_(Users.is_deleted == False, Users.is_deleted == 0))
    #         # В SQLAlchemy условие выборки должно быть записано без использования Python-оператора not.
    #
    #         result_tmp = await pool.execute(query)
    #         results = result_tmp.scalars().all()  #






