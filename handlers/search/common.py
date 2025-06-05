from aiogram.types import Message
from keyboards import get_back_button, get_game_menu
from services.rawg_games import RAWGGamesService
from logger_config import log_info, log_error, log_bot, log_user

rawg_client = RAWGGamesService()

async def search_games(message: Message, query: str, index: int = 0, search_type: str = 'name', original_user_id=None, original_username=None):
    user_id = original_user_id or message.from_user.id
    username = original_username or message.from_user.username
    
    if index == 0:
        search_msg = await message.answer("🔍 Ищу игры...")
        log_info(f"Начат поиск игр для пользователя {user_id}: '{query}', тип: {search_type}")
    else:
        log_info(f"Навигация по результатам поиска для пользователя {user_id}: '{query}', индекс: {index}")
    
    try:
        games = await rawg_client.search_games(query, limit=10, search_type=search_type)
        
        if not games or index >= len(games):
            if index == 0:
                search_text = ""
                if search_type == 'name':
                    search_text = f"по названию '{query}'"
                elif search_type == 'genre':
                    search_text = f"по жанру '{query}'"
                elif search_type == 'tag':
                    search_text = f"по тегу '{query}'"
                
                no_results = f"😔 Игры {search_text} не найдены."
                
                log_info(f"Поиск для пользователя {user_id} не дал результатов: '{query}', тип: {search_type}")
                
                if hasattr(search_msg, 'edit_text'):
                    await search_msg.edit_text(no_results, reply_markup=get_back_button())
                else:
                    await message.answer(no_results, reply_markup=get_back_button())
                
                log_bot(user_id, no_results)
            else:
                end_msg = "🔚 Больше игр по этому запросу не найдено."
                log_info(f"Достигнут конец результатов для пользователя {user_id}: '{query}', индекс: {index}")
                await message.answer(
                    end_msg,
                    reply_markup=get_back_button()
                )
                log_bot(user_id, end_msg)
            return

        if index == 0 and hasattr(search_msg, 'delete'):
            await search_msg.delete()

        game = games[index]
        
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
 
        log_info(f"Поиск для пользователя {user_id} дал {len(games)} результатов: '{query}', тип: {search_type}")
        log_user(user_id, username, f"Просматривает игру '{name}' (ID: {game_id}), результат {index + 1} из {len(games)}")

        result_text = (
            f"**{name}**\n\n"
            f"⭐ Рейтинг: {rating}/5\n"
            f"📅 Дата выхода: {released}\n"
            f"🎯 Платформы: {platforms_text}\n"
            f"🏷️ Теги: {tags_text}\n\n"
            f"🔢 Результат {index + 1} из {len(games)}"
        )

        try:
            if image_url:
                await message.answer_photo(
                    photo=image_url,
                    caption=result_text,
                    reply_markup=get_game_menu(game_id, query, index, len(games), search_type),
                    parse_mode='Markdown'
                )
                log_bot(user_id, result_text)
            else:
                await message.answer(
                    text=result_text,
                    reply_markup=get_game_menu(game_id, query, index, len(games), search_type),
                    parse_mode='Markdown'
                )
                log_bot(user_id, result_text)
        except Exception as e:
            log_error(f"Ошибка при отображении игры {name} для пользователя {user_id}: {str(e)}")
            await message.answer(
                text=result_text,
                reply_markup=get_game_menu(game_id, query, index, len(games), search_type),
                parse_mode='Markdown'
            )
            log_bot(user_id, result_text)

    except Exception as e:
        error_text = f'Произошла ошибка при поиске игр. Попробуйте позже.'
        log_error(f"Ошибка при поиске игр для пользователя {user_id}: '{query}', тип '{search_type}' - {str(e)}")
        await message.answer(error_text, reply_markup=get_back_button())
        log_bot(user_id, error_text) 
