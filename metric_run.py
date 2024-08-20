"""
metric_bot
"""

# -------------------------------- Стандартные модули
import os
import asyncio
# import logging
# logging.basicConfig(level=logging.INFO)
# -------------------------------- Сторонние библиотеки
from aiogram import types, Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties  # Обработка текста HTML разметкой

# from aiogram import types, Router, F

# -------------------------------- Локальные модули

from dotenv import find_dotenv, load_dotenv  # Для переменных окружения
load_dotenv(find_dotenv())  # Загружаем переменную окружения

from handlers.metric_handler import metric
from db_connect.async_engine import *
from db_connect.middlewares import *


# ----------------------------------------------------------------------------------------------------------------------
bot: Bot = Bot(token=os.getenv('API_TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))

# --------------------------------------------- Инициализация диспетчера событий
# Принимает все события и отвечает за порядок их обработки в асинхронном режиме.
dp = Dispatcher()
dp.include_router(metric) # Назначаем роутеры:
# -------------------------------------------------- Тело бота:




# ---------------------------------------------------- Зацикливание работы бота
# Отслеживание событий на сервере тг бота:
async def run_bot():


    # ------------------------------------------------------------------------------------
    async def on_startup(bot):
        # Удаление Webhook и всех ожидающих обновлений
        await bot.delete_webhook(drop_pending_updates=True)
        print("Webhook удален и ожидающие обновления сброшены.")



    async def on_shutdown(bot):
        async def shutdown_on():
            """
                Корректное завершение работы вашего бота (stop_polling).
                Вызовите метод stop_polling: Если вы используете метод длительного опроса (start_polling)
                для получения обновлений от серверов Telegram, убедитесь, что вы вызываете метод stop_polling
                при завершении работы вашего бота. Это позволит корректно завершить процесс опроса серверов Telegram.
            """
            await dp.stop_polling()
            await asyncio.sleep(1)
            await dp.storage.close()
            await bot.close() # Закрытие сессии бота при завершении работы

            print('Бот лег!')



    # ---------------------
    dp.startup.register(on_startup)  # действия при старте бота +
    dp.shutdown.register(on_shutdown)  # действия при остановке бота +

    # -------------------------------------------------------------------------------
    # Установка промежуточного слоя (сразу для диспетчера, не для роутеров):
    # dp.update.middleware(DataBaseSession(session=session_JAR)) - для одной бд (сессии)

    # Для нескольких сессий (подключения к нескольким бд):
    dp.update.middleware(AllSessionDB(session_jar=session_JAR, session_mart_sv=session_MART_SV,
        session_gp_mart_sv=session_GP_MART_SV))



    await bot.delete_webhook(drop_pending_updates=True)  # Сброс отправленных сообщений, за время, что бот был офлайн.
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # todo если надо удалить  команды из меню.


    await dp.start_polling(
        bot, skip_updates=True, polling_timeout = 3, handle_signals=True,  close_bot_session = True,
         allowed_updates=['message', 'edited_message', 'callback_query'] # handle_as_tasks=True,
    )


# Запуск асинхронной функции run_bot:
if __name__ == "__main__":
    asyncio.run(run_bot())


