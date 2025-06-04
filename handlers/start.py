from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import get_main_menu, get_back_button
from logger_config import log_user, log_bot, log_error

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    log_user(user_id, username, "Выполнил команду /start")

    welcome_text = (
        f"🎮 Добро пожаловать в RAWGbot, {message.from_user.first_name}!\n\n"
        "Я помогу вам найти информацию об играх, получить список популярных игр и многое другое!\n\n"
        "Выберите действие из меню ниже:"
    )

    await message.answer(welcome_text, reply_markup=get_main_menu())

    log_bot(user_id, welcome_text)

@router.message(Command("help"))
async def help_commnad(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    log_user(user_id, username, "Выполнил команду /help")

    help_text = (
        "Доступные команды:\n\n"
        "/start - Запустить бота и показать главное меню\n"
        "/help - Показать справку по командам\n"
        "/search [название] - Поиск игры по названию\n"
        "/popular - Показать популярные игры\n"
        "/random - Показать случайную игру\n\n"
        "Также вы можете использовать кнопки в меню для навигации"
        )

    await message.answer(help_text, reply_markup=get_back_button())

    log_bot(user_id, help_text)

@router.callback_query(F.data == 'help')
async def help_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username

    log_user(user_id, username, "Нажал на кнпоку 'Помощь'")

    help_text = (
        "Доступные команды:\n\n"
        "/start - Запустить бота и показать главное меню\n"
        "/help - Показать справку по командам\n"
        "/search [название] - Поиск игры по названию\n"
        "/popular - Показать популярные игры\n"
        "/random - Показать случайную игру\n\n"
        "Также вы можете использовать кнопки в меню для навигации"
        )

    await callback.message.edit_text(help_text, reply_markup=get_back_button())

    log_bot(user_id, help_text)

@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username

    log_user(user_id, username, "Вернулся в главное меню")

    welcome_text = (
        "🎮 Главное меню GameBot\n\n"
        "Ваш персональный помощник и гид в безграничном мире видеоигр!\n\n"
        "Выберите действие:"
    )

    try:
        await callback.message.delete()
        await callback.message.answer(
            welcome_text, 
            reply_markup=get_main_menu()
        )

        log_bot(user_id, welcome_text)
        
    except Exception as e:
        log_error(f"Ошибка при возврате в главное меню для пользователя {user_id}: {str(e)}")
        await callback.message.answer(
            welcome_text, 
            reply_markup=get_main_menu()
        )
