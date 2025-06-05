import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start, search, popular, random, details
from logger_config import log_info, log_error


async def main():
    storage = MemoryStorage()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    dp.include_router(start)
    dp.include_router(search)
    dp.include_router(popular)
    dp.include_router(random)
    dp.include_router(details)

    log_info("Обработчики зарегистрированы")

    try:
        log_info("Бот запущен")
        log_info("Поллинг запущен")
        await dp.start_polling(bot)
    except Exception as e:
        log_error(f"Ошибка в процессе работы бота: {e}", exc_info=True)
    finally:
        log_info("Завершение работы бота")
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
