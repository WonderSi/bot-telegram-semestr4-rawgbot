from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import get_back_button
from handlers.search.states import SearchStates
from keyboards import get_search_type_menu
from logger_config import log_user, log_bot, log_info, log_error

router = Router()

@router.callback_query(F.data == "search_games")
async def search_games_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    log_user(user_id, username, "Нажал на кнопку 'Поиск игр'")

    prompt_text = "🔍 Выберите тип поиска:"

    try:
        await callback.message.delete()
    except Exception as e:
        log_error(f"Не удалось удалить сообщение для пользователя {user_id}: {str(e)}")
    
    await callback.message.answer(prompt_text, reply_markup=get_search_type_menu())
    log_bot(user_id, prompt_text)

@router.callback_query(F.data == "search_by_name")
async def search_by_name_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    log_user(user_id, username, "Выбрал поиск по названию")

    prompt_text = "🔍 Введите название игры для поиска:"

    try:
        await callback.message.delete()
    except Exception as e:
        log_error(f"Не удалось удалить сообщение для пользователя {user_id}: {str(e)}")
    
    await callback.message.answer(prompt_text, reply_markup=get_back_button())
    log_bot(user_id, prompt_text)
    
    await state.set_state(SearchStates.waiting_for_game_name)
    log_info(f"Пользователь {user_id} переведен в состояние ожидания ввода названия игры")

@router.callback_query(F.data == "search_by_genre")
async def search_by_genre_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    log_user(user_id, username, "Выбрал поиск по жанру")

    prompt_text = (
        "🎭 Введите название жанра для поиска:\n\n"
        "Примеры жанров: action, adventure, rpg, strategy, shooter, racing, puzzle, sports, platformer"
    )

    try:
        await callback.message.delete()
    except Exception as e:
        log_error(f"Не удалось удалить сообщение для пользователя {user_id}: {str(e)}")

    await callback.message.answer(prompt_text, reply_markup=get_back_button())
    log_bot(user_id, prompt_text)
    
    await state.set_state(SearchStates.waiting_for_genre)
    log_info(f"Пользователь {user_id} переведен в состояние ожидания ввода жанра")

@router.callback_query(F.data == "search_by_tag")
async def search_by_tag_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    log_user(user_id, username, "Выбрал поиск по тегу")

    prompt_text = (
        "🏷️ Введите тег для поиска:\n\n"
        "Примеры тегов: multiplayer, singleplayer, open-world, fps, sci-fi, fantasy"
    )

    try:
        await callback.message.delete()
    except Exception as e:
        log_error(f"Не удалось удалить сообщение для пользователя {user_id}: {str(e)}")
    
    await callback.message.answer(prompt_text, reply_markup=get_back_button())
    log_bot(user_id, prompt_text)
    
    await state.set_state(SearchStates.waiting_for_tag)
    log_info(f"Пользователь {user_id} переведен в состояние ожидания ввода тега") 
