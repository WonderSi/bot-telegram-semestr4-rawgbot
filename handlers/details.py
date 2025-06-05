from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards import get_back_button, get_detail_search_menu, get_detail_popular_menu, get_detail_random_menu
from services.rawg_games import RAWGGamesService
from logger_config import log_user, log_bot, log_info, log_error

router = Router()
rawg_client = RAWGGamesService()


@router.callback_query(F.data.startswith("details_") & ~F.data.startswith("details_popular_") & ~F.data.startswith("details_random_"))
async def details_search_game_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username

    try:
        game_id = int(callback.data.split("_")[1])

        log_user(user_id, username,
                 f"Запросил детали игры с ID {game_id} (из поиска)")
        await callback.answer("Загружаю подробную информацию...")

        try:
            await callback.message.delete()
        except Exception as e:
            log_error(
                f"Не удалось удалить предыдущее сообщение для пользователя {user_id}: {str(e)}")
            pass

        await show_game_details(callback, game_id, "search", original_user_id=user_id, username=username)
    except Exception as e:
        log_error(
            f"Ошибка при обработке запроса деталей игры (из поиска) для пользователя {user_id}: {str(e)}")
        await callback.message.answer(
            "Произошла ошибка при получении информации об игре",
            reply_markup=get_back_button()
        )
        log_bot(user_id, "Произошла ошибка при получении информации об игре")


@router.callback_query(F.data.startswith("details_popular_"))
async def details_popular_game_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username

    try:
        game_id = int(callback.data.split("_")[2])

        log_user(user_id, username,
                 f"Запросил детали игры с ID {game_id} (из популярных)")
        await callback.answer("Загружаю подробную информацию...")

        try:
            await callback.message.delete()
        except Exception as e:
            log_error(
                f"Не удалось удалить предыдущее сообщение для пользователя {user_id}: {str(e)}")
            pass

        await show_game_details(callback, game_id, "popular", original_user_id=user_id, username=username)
    except Exception as e:
        log_error(
            f"Ошибка при обработке запроса деталей игры (из популярных) для пользователя {user_id}: {str(e)}")
        await callback.message.answer(
            "Произошла ошибка при получении информации об игре",
            reply_markup=get_back_button()
        )
        log_bot(user_id, "Произошла ошибка при получении информации об игре")


@router.callback_query(F.data.startswith("details_random_"))
async def details_random_game_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username

    try:
        game_id = int(callback.data.split("_")[2])

        log_user(user_id, username,
                 f"Запросил детали игры с ID {game_id} (из случайных)")
        await callback.answer("Загружаю подробную информацию...")

        try:
            await callback.message.delete()
        except Exception as e:
            log_error(
                f"Не удалось удалить предыдущее сообщение для пользователя {user_id}: {str(e)}")
            pass

        await show_game_details(callback, game_id, "random", original_user_id=user_id, username=username)
    except Exception as e:
        log_error(
            f"Ошибка при обработке запроса деталей игры (из случайных) для пользователя {user_id}: {str(e)}")
        await callback.message.answer(
            "Произошла ошибка при получении информации об игре",
            reply_markup=get_back_button()
        )
        log_bot(user_id, "Произошла ошибка при получении информации об игре")


async def show_game_details(callback: CallbackQuery, game_id: int, source_type: str, original_user_id=None, username=None):
    user_id = original_user_id or callback.from_user.id
    current_username = username or callback.from_user.username

    try:
        log_info(
            f"Загрузка деталей игры {game_id} для пользователя {user_id} (тип: {source_type})")
        log_user(user_id, current_username,
                 f"Запросил детали игры (ID: {game_id})")

        game_details = await rawg_client.get_game_details(game_id)

        if not game_details:
            log_error(
                f"Не удалось получить информацию об игре {game_id} для пользователя {user_id}")

            await callback.message.answer(
                "Не удалось получить информацию об игре",
                reply_markup=get_back_button()
            )

            log_bot(user_id, "Не удалось получить информацию об игре")
            return

        name = game_details.get('name', 'Нет названия')
        description_raw = game_details.get(
            'description_raw', 'Описание отсутствует')
        description = description_raw[:500] + \
            "..." if len(description_raw) > 500 else description_raw
        rating = game_details.get('rating', 'N/A')
        metacritic = game_details.get('metacritic', 'N/A')
        released = game_details.get('released', 'Неизвестно')
        genres = [genre['name'] for genre in game_details.get('genres', [])]
        genres_text = ', '.join(genres[:3]) if genres else 'Не указаны'

        tags = [tag['name'] for tag in game_details.get('tags', [])[:5]]
        tags_text = ', '.join(tags) if tags else 'Не указаны'

        log_info(f"Загружены детали игры '{name}' для пользователя {user_id}")

        detailed_text = (
            f"🎮 **{name}**\n\n"
            f"⭐ Рейтинг: {rating}/5\n"
            f"🏆 Metacritic: {metacritic}\n"
            f"📅 Дата выхода: {released}\n"
            f"🎯 Жанры: {genres_text}\n"
            f"🏷️ Теги: {tags_text}\n\n"
            f"📝 **Описание:**\n{description}"
        )

        if source_type == "search":
            reply_markup = get_detail_search_menu()
        elif source_type == "popular":
            reply_markup = get_detail_popular_menu()
        elif source_type == "random":
            reply_markup = get_detail_random_menu()
        else:
            reply_markup = get_back_button()

        image_url = game_details.get('background_image')

        if image_url:
            await callback.message.answer_photo(
                photo=image_url,
                caption=detailed_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await callback.message.answer(
                detailed_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )

        log_bot(user_id, f"Отправлены детали игры: {name}")

    except Exception as e:
        log_error(
            f"Ошибка при получении деталей игры {game_id} для пользователя {user_id}: {str(e)}")

        await callback.message.answer(
            "Произошла ошибка при получении информации об игре",
            reply_markup=get_back_button()
        )

        log_bot(user_id, "Произошла ошибка при получении информации об игре")
