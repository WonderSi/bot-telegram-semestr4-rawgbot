from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import get_random_game_menu, get_back_button
from services.rawg_games import RAWGGamesService
from logger_config import log_user, log_bot, log_info, log_error

router = Router()
rawg_client = RAWGGamesService()

last_random_game = None

@router.message(Command("random"))
async def random_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    log_user(user_id, username, "Выполнил команду /random")
    
    loading_message = await message.answer("🎲 Ищу случайную игру...")
    log_bot(user_id, "🎲 Ищу случайную игру...")
    
    await show_random_game(loading_message, original_user_id=user_id, username=username)
    
@router.callback_query(F.data == "random_game")
async def random_game_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    log_user(user_id, username, "Нажал на кнопку 'Случайная игра'")
    
    await callback.answer("Ищу случайную игру...")
    
    try:
        await callback.message.delete()
        loading_message = await callback.message.answer("🎲 Ищу случайную игру...")
        log_bot(user_id, "🎲 Ищу случайную игру...")
        await show_random_game(loading_message, original_user_id=user_id, username=username)
    except Exception as e:
        log_error(f"Ошибка при отображении сообщения о загрузке для пользователя {user_id}: {str(e)}")
        await show_random_game(callback.message, original_user_id=user_id, username=username)

@router.callback_query(F.data == "back_to_random")
async def back_to_random_callback(callback: CallbackQuery):
    global last_random_game
    
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    log_user(user_id, username, "Вернулся к случайной игре")
    
    try:
        await callback.message.delete()
        
        if last_random_game:
            log_info(f"Показываем кэшированную случайную игру для пользователя {user_id}")
            await show_random_game_from_data(callback.message, last_random_game, original_user_id=user_id, username=username)
        else:
            log_info(f"Кэш пуст, ищем новую случайную игру для пользователя {user_id}")
            loading_message = await callback.message.answer("🎲 Ищу случайную игру...")
            log_bot(user_id, "🎲 Ищу случайную игру...")
            await show_random_game(loading_message, original_user_id=user_id, username=username)
    except Exception as e:
        log_error(f"Ошибка при возврате к случайной игре для пользователя {user_id}: {str(e)}")
        await callback.message.answer(
            "Произошла ошибка при возврате к игре. Попробуйте найти новую случайную игру.",
            reply_markup=get_back_button()
        )
        log_bot(user_id, "Произошла ошибка при возврате к игре. Попробуйте найти новую случайную игру.")

async def show_random_game_from_data(message, game, original_user_id=None, username=None):
    """Отображает случайную игру из уже полученных данных"""
    user_id = original_user_id or (message.from_user.id if hasattr(message, 'from_user') else None)
    
    try:
        name = game.get('name', 'Нет названия')
        rating = game.get('rating', 'N/A')
        released = game.get('released', 'Неизвестно')
        platforms = [platform['platform']['name'] for platform in game.get('platforms', [])]
        platforms_text = ', '.join(platforms[:3])
        if len(platforms) > 3:
            platforms_text += f" и еще {len(platforms)-3}"
            
        tags = []
        for tag in game.get('tags', [])[:3]:
            tags.append(tag.get('name', ''))
        tags_text = ', '.join(tags) if tags else 'Нет тегов'
        
        image_url = game.get('background_image')
        game_id = game.get('id')
        
        result_text = (
            f"🎲 **{name}**\n\n"
            f"⭐ Рейтинг: {rating}/5\n"
            f"📅 Дата выхода: {released}\n"
            f"🎯 Платформы: {platforms_text}\n"
            f"🏷️ Теги: {tags_text}\n"
        )
        
        if user_id:
            log_info(f"Пользователь {user_id} просматривает случайную игру '{name}' (ID: {game_id})")
            if username:
                log_user(user_id, username, f"Просматривает случайную игру '{name}'")
        
        if image_url:
            await message.answer_photo(
                photo=image_url,
                caption=result_text,
                reply_markup=get_random_game_menu(game_id),
                parse_mode='Markdown'
            )
        else:
            await message.answer(
                result_text,
                reply_markup=get_random_game_menu(game_id),
                parse_mode='Markdown'
            )
            
        if user_id:
            log_bot(user_id, f"Отображена случайная игра: {name}")
    except Exception as e:
        if user_id:
            log_error(f"Ошибка при отображении случайной игры для пользователя {user_id}: {str(e)}")
        await message.answer(
            "Произошла ошибка при отображении игры. Попробуйте найти новую случайную игру.",
            reply_markup=get_back_button()
        )
        if user_id:
            log_bot(user_id, "Произошла ошибка при отображении игры. Попробуйте найти новую случайную игру.")

async def show_random_game(message, original_user_id=None, username=None):
    global last_random_game
    
    user_id = original_user_id or message.from_user.id
    
    try:
        if user_id:
            log_info(f"Поиск случайной игры для пользователя {user_id}")
            if username:
                log_user(user_id, username, f"Запросил случайную игру")
            
        game = await rawg_client.get_random_game()
        
        if not game:
            error_text = "😔 Не удалось найти случайную игру. Попробуйте позже."
            
            if user_id:
                log_error(f"Не удалось найти случайную игру для пользователя {user_id}")
            
            if hasattr(message, 'edit_text'):
                await message.edit_text(error_text, reply_markup=get_back_button())
            else:
                await message.answer(error_text, reply_markup=get_back_button())
                
            if user_id:
                log_bot(user_id, error_text)
            return
        
        last_random_game = game
        
        if user_id:
            log_info(f"Найдена случайная игра '{game.get('name', 'Нет названия')}' для пользователя {user_id}")
        
        if hasattr(message, 'delete'):
            await message.delete()
        
        await show_random_game_from_data(message, game, original_user_id=user_id, username=username)
                
    except Exception as e:
        error_text = "Произошла ошибка при поиске случайной игры. Попробуйте позже."
        
        if user_id:
            log_error(f"Ошибка при поиске случайной игры для пользователя {user_id}: {str(e)}")
        
        if hasattr(message, 'edit_text'):
            await message.edit_text(error_text, reply_markup=get_back_button())
        else:
            await message.answer(error_text, reply_markup=get_back_button()) 
            
        if user_id:
            log_bot(user_id, error_text) 
