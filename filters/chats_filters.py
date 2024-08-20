"""
Модуль фильтрации роутеров.
Фильтрует события, в зависимости от того в каком чате было написано сообщение.

Кастомный класс наследуется из класса Filter.

Важно:
Тип чата может быть “приватным”, ”групповым“, ”супергрупповым“ или "каналом” - >
( “private”, “group”, “supergroup”, “channel”)
см.: https://core.telegram.org/bots/api#chat
"""

from aiogram.filters import Filter

#
#
# from aiogram import types, Bot
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.ext.asyncio.engine import AsyncEngine
# from sqlalchemy.ext.asyncio import AsyncSession
# from aiogram.types import Message, TelegramObject
# from typing import Any, Awaitable, Callable, Dict, Union
#
#
# # ----------------------------------------------------------------------------------------------------------------------
# # chats_filters
# class ChatTypeFilter(Filter):
#     """Для фильтрации ипа приватности (групповой чат или приватный или супер приватный"""
#
#     # Сюда передаем список имен чартов:
#     def __init__(self, chat_types: list[str]) -> None:
#         self.chat_types = chat_types
#
#     # Здесь выдает соответствие типу чата в котором было сообщение (тру если соответствует названию) или нет
#     async def __call__(self, message: types.Message) -> bool:
#         return message.chat.type in self.chat_types

