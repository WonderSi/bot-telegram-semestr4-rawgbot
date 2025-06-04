from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards import get_back_button
from handlers.search.common import search_games
from logger_config import log_user, log_info, log_error

router = Router()

@router.callback_query(F.data.startswith("search_next_"))
async def next_result(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    try:
        # Парсим данные из callback_data
        parts = callback.data.split('_')
        query = parts[2]
        index = int(parts[3])
        max_results = int(parts[4])
        search_type = parts[5] if len(parts) > 5 else 'name'
        
        if index < max_results - 1:
            log_user(user_id, username, f"Запросил следующий результат поиска '{query}', индекс {index+1}")
            await callback.answer("Загружаю следующий результат...")
            
            # Удаляем предыдущее сообщение перед отправкой нового
            try:
                await callback.message.delete()
            except Exception as e:
                log_error(f"Не удалось удалить предыдущее сообщение для пользователя {user_id}: {str(e)}")
            
            await search_games(callback.message, query, index + 1, search_type, original_user_id=user_id, original_username=username)
        else:
            log_info(f"Пользователь {user_id} достиг конца результатов поиска '{query}'")
            await callback.answer("Больше результатов нет", show_alert=True)
    except Exception as e:
        log_error(f"Ошибка при навигации по результатам поиска для пользователя {user_id}: {str(e)}")
        await callback.answer("Произошла ошибка при загрузке следующего результата", show_alert=True)
        await callback.message.answer(
            "Произошла ошибка при навигации по результатам поиска",
            reply_markup=get_back_button()
        )
