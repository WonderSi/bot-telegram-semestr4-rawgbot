from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    welcome_text = (
        f"🎮 Добро пожаловать в RAWGbot, {message.from_user.first_name}!\n\n"
        "Я помогу вам найти информацию об играх, получить список популярных игр и многое другое!\n\n"
        "Выберите действие из меню ниже:"

    )

    await message.answer(welcome_text)
