from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from kb import get_main_menu
from logger import dialog_logger

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    dialog_logger.log_user_message(user_id, username, "/start")

    welcome_text = (
        f"🎮 Добро пожаловать в RAWGbot, {message.from_user.first_name}!\n\n"
        "Я помогу вам найти информацию об играх, получить список популярных игр и многое другое!\n\n"
        "Выберите действие из меню ниже:"

    )

    dialog_logger.log_bot_messag(user_id, welcome_text)

    await message.answer(welcome_text, reply_markup=get_main_menu())

@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    user_id = callback.from_user.id

    dialog_logger.get_user_logger(user_id, callback.from_user.username, "Возврат в главное меню")

    welcome_text = (
        "🎮 Главное меню GameBot\n\n"
        "Выберите действие:"
    )

    dialog_logger.get_bot_logger(user_id, welcome_text)

    await callback.message.edit_text(welcome_text, reply_markup=get_main_menu())
