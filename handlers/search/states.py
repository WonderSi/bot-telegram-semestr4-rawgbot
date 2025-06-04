from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.search.common import search_games
from logger_config import log_user, log_info

router = Router()

class SearchStates(StatesGroup):
    waiting_for_game_name = State()
    waiting_for_genre = State()
    waiting_for_tag = State()

@router.message(StateFilter(SearchStates.waiting_for_game_name))
async def process_game_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    
    game_name = message.text.strip()
    
    log_user(user_id, username, f"Ввел название игры для поиска: '{game_name}'")
    log_info(f"Пользователь {user_id} выполняет поиск по названию: '{game_name}'")
    
    await state.clear()
    
    await search_games(message, game_name, 0, 'name', original_user_id=user_id, original_username=username)

@router.message(StateFilter(SearchStates.waiting_for_genre))
async def process_genre(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    
    genre = message.text.strip()
    
    log_user(user_id, username, f"Ввел жанр для поиска: '{genre}'")
    log_info(f"Пользователь {user_id} выполняет поиск по жанру: '{genre}'")
    
    await state.clear()
    
    await search_games(message, genre, 0, 'genre', original_user_id=user_id, original_username=username)

@router.message(StateFilter(SearchStates.waiting_for_tag))
async def process_tag(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    
    tag = message.text.strip()
    
    log_user(user_id, username, f"Ввел тег для поиска: '{tag}'")
    log_info(f"Пользователь {user_id} выполняет поиск по тегу: '{tag}'")
    
    await state.clear()
    
    await search_games(message, tag, 0, 'tag', original_user_id=user_id, original_username=username) 
