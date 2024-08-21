"""
Модуль содержит функции создания подключения к базам данных.


!!! Обязательно в конфиге CONFIG_JAR_DRIVERNAME=postgresql+asyncpg.
!!!! Обязательна установка библиотеки asyncpg.

"""

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------- Импорт стандартных библиотек Пайтона
import os
# import logging
# import pprint


# ---------------------------------- Импорт сторонних библиотек
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.engine.url import URL

# -------------------------------- Локальные модули
from settings.configs import *


# ----------------------------------------------------------------------------------------------------------------------
# Создаем URL строку:
def get_url_string(ANY_CONFIG: dict | URL | str) -> object:

    # Проверка типа входной конфигурации подключения:
    # Если на вход конфигурация в словаре:
    if isinstance(ANY_CONFIG, dict) == True:
        url_string = URL.create(**ANY_CONFIG)  # 1. Формируем URL-строку соединения с БД.
        #  Эквивалент: url_string = (f'{drivername}://{username}:{password}@{host}:{port}/{database}')

    # Если на вход url_string:
    elif isinstance(ANY_CONFIG, str) == True:
        url_string = ANY_CONFIG
    else:
        url_string = None

    return url_string   # return create_async_engine(url_string)





# ------------------------------------------- Создаем общую сессию для всех модулей: !!!
url_string_jar = get_url_string(URL_STRING_JAR_ASYNCPG)
url_string_mart_sv = get_url_string(URL_STRING_MART_SV_ASYNCPG)
url_string_gp_mart_sv = get_url_string(URL_STRING_GP_MART_SV_ASYNCPG)


engine_jar = create_async_engine(url_string_jar) # , echo=True (Для логирования)!
engine_mart_sv = create_async_engine(url_string_mart_sv)
engine_gp_mart_sv = create_async_engine(url_string_gp_mart_sv)

# Создаем сесии:
session_JAR = async_sessionmaker(bind=engine_jar, class_=AsyncSession, expire_on_commit=False) #
session_MART_SV = async_sessionmaker(bind=engine_mart_sv, class_=AsyncSession, expire_on_commit=False) #
session_GP_MART_SV = async_sessionmaker(bind=engine_gp_mart_sv, class_=AsyncSession, expire_on_commit=False) #




