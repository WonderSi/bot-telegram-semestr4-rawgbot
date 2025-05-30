from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from kb import get_back_button
from rawg_api import RAWGClient

router = Router()
rawg_client = RAWGClient()

class SearchStates(StatesGroup):
    waiting_for_game_name = State()


@router.message(Command("search"))
async def search_commnad(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"

    args = message.text.split(maxsplit=1)

    if len(args) > 1:
        game_name = args[1]
        await search_games(message, game_name)
    else:
        prompt_text = "Введите название игры для поиска"
        await message.answer(prompt_text, reply_markup=get_back_button())
        await state.set_state(SearchStates.waiting_for_game_name)

@router.message(SearchStates.waiting_for_game_name)
async def process_game_search(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    game_name = message.text

    await search_games(message, game_name)
    await state.clear()
    
async def search_games(message: Message, game_name: str):
    user_id = message.from_user.id
    search_msg = await message.answer("Ищу игры...")
    try:
        games = await rawg_client.search_games(game_name, limit=3)
        
        if not games:
            no_results = f"Игры с название '{game_name}' не найдены"

            await search_msg.edit_text(no_results, reply_markup=get_back_button())

        result_text = f"Найдено игр по запросу '{game_name}':\n\n"

        for i, game in  enumerate(games, 1):
            rating = game.get('rating', 'N/A')
            released = game.get('released', 'Неизвестно')
            platforms = [platform['platform']['name'] for platform in game.get('platforms', [])]
            platforms_text = ', '.join(platforms[:3])
            if len(platforms) > 3:
                platforms_text += f" и еще {len(platforms)-3}"

            result_text += (
                f"{i}. **{game['name']}**\n"
                f"Рейтинг: {rating}/5\n"
                f"Дата выхода: {released}\n"
                f"Платформы: {platforms_text}\n\n"
            )

        await search_msg.edit_text(
            result_text,
            reply_markup=get_back_button(),
            parse_mode='Markdown'
        )
    except Exception as e:
        error_text = f'Произошла ошибка при поиске игр. Попробуйте позже.'
        await search_msg.edit_text(error_text)
