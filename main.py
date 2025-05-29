import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN

async def main():
    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher()

    print("Бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
