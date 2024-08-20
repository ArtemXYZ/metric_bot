"""
Модуль "ПРОМЕЖУТОЧНЫХ СЛОЕВ" содержит пользовательские классы необходимых в дальнейшем
для работы с базами данных (SQL запросов).
"""

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------- Импорт стандартных библиотек Пайтона
# ---------------------------------- Импорт сторонних библиотек
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker
from aiogram.types import Message, TelegramObject
from typing import Any, Awaitable, Callable, Dict
# ---------------------------------- Импорт сторонних библиотек
# from metric_run import bot

# ----------------------------------------------------------------------------------------------------------------------
# Middleware для передачи бота в хендлеры:
class BotMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data['bot'] = bot
        return await handler(event, data)



# Промежуточный слой для одной сессии:
# class DataBaseSession(BaseMiddleware):
#     def __init__(self, session: async_sessionmaker):  #
#         self.session = session
#
#     async def __call__(
#             self,
#             handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#             event: TelegramObject,
#             data: Dict[str, Any],
#     ) -> Any:
#         async with self.session() as session:
#             data['session'] = session  # Передаем в словарь переменную, которая будет доступна в хендлерах.
#             return await handler(event, data)










# Промежуточный слой для нескольких сессий:
class AllSessionDB(BaseMiddleware):
    def __init__(self, session_jar: async_sessionmaker, session_mart_sv: async_sessionmaker,
                 session_gp_mart_sv: async_sessionmaker):

        self.session_jar = session_jar
        self.session_mart_sv = session_mart_sv
        self.session_gp_mart_sv = session_gp_mart_sv

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_jar() as session_jar, self.session_mart_sv() as session_mart_sv, \
            self.session_gp_mart_sv() as session_gp_mart_sv:
            data['session_jar'] = session_jar
            data['session_mart_sv'] = session_mart_sv
            data['session_gp_mart_sv'] = session_gp_mart_sv

            return await handler(event, data)