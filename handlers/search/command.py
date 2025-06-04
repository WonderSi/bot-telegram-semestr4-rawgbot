from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import get_search_type_menu
from handlers.search.common import search_games
from logger_config import log_user, log_bot

router = Router()


@router.message(Command("search"))
async def search_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    args = message.text.split(maxsplit=1)

    if len(args) > 1:
        game_name = args[1]
        log_user(user_id, username, f"Выполнил команду /search {game_name}")
        await search_games(message, game_name, 0, 'name', original_user_id=user_id, original_username=username)
    else:
        log_user(user_id, username, "Выполнил команду /search без параметров")
        log_bot(user_id, prompt_text)
        prompt_text = "🔍 Выберите тип поиска:"
        await message.answer(prompt_text, reply_markup=get_search_type_menu())
