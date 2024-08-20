"""
Все конфиги проекта
"""
# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------- Импорт стандартных библиотек Пайтона
import os

# ---------------------------------- Импорт сторонних библиотек
from dotenv import find_dotenv, load_dotenv  # Для переменных окружения
load_dotenv(find_dotenv())  # Загружаем переменную окружения

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------- Конфигурации подключения к базам данных
# CONFIG_JAR = {
#     'drivername': os.environ.get("CONFIG_JAR_DRIVERNAME"),
#     'username': os.environ.get("CONFIG_JAR_USERNAME"),
#     'password': os.environ.get("CONFIG_JAR_PASSWORD"),
#     'host': os.environ.get("CONFIG_JAR_HOST"),
#     'port': os.environ.get("CONFIG_JAR_PORT"),
#     'database': os.environ.get("CONFIG_JAR_DATABASE")
# }

URL_STRING_JAR_ASYNCPG = {
    'drivername': os.environ.get("CONFIG_JAR_DRIVERNAME_ASYNCPG"),
    'username': os.environ.get("CONFIG_JAR_USERNAME"),
    'password': os.environ.get("CONFIG_JAR_PASSWORD"),
    'host': os.environ.get("CONFIG_JAR_HOST"),
    'port': os.environ.get("CONFIG_JAR_PORT"),
    'database': os.environ.get("CONFIG_JAR_DATABASE")
}


# CONFIG_MART_SV = {
#     'drivername': os.environ.get("CONFIG_MART_SV_DRIVERNAME"),
#     'username': os.environ.get("CONFIG_MART_SV_USERNAME"),
#     'password': os.environ.get("CONFIG_MART_SV_PASSWORD"),
#     'host': os.environ.get("CONFIG_MART_SV_HOST"),
#     'port': os.environ.get("CONFIG_MART_SV_PORT"),
#     'database': os.environ.get("CONFIG_MART_SV_DATABASE")
# }


URL_STRING_MART_SV_ASYNCPG = {
    'drivername': os.environ.get("CONFIG_MART_SV_DRIVERNAME_ASYNCPG"),
    'username': os.environ.get("CONFIG_MART_SV_USERNAME"),
    'password': os.environ.get("CONFIG_MART_SV_PASSWORD"),
    'host': os.environ.get("CONFIG_MART_SV_HOST"),
    'port': os.environ.get("CONFIG_MART_SV_PORT"),
    'database': os.environ.get("CONFIG_MART_SV_DATABASE")
}

URL_STRING_GP_MART_SV_ASYNCPG = {
    'drivername': os.environ.get("CONFIG_GP_MART_SV_DRIVERNAME_ASYNCPG"),
    'username': os.environ.get("CONFIG_GP_MART_SV_USERNAME"),
    'password': os.environ.get("CONFIG_GP_MART_SV_PASSWORD"),
    'host': os.environ.get("CONFIG_GP_MART_SV_HOST"),
    'port': os.environ.get("CONFIG_GP_MART_SV_PORT"),
    'database': os.environ.get("CONFIG_GP_MART_SV_DATABASE")
}

