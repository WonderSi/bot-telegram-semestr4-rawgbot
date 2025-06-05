from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import get_back_button, get_popular_games_menu
from services.rawg_games import RAWGGamesService
from logger_config import log_user, log_bot, log_info, log_error

router = Router()
rawg_client = RAWGGamesService()


@router.message(Command("popular"))
async def popular_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"

    log_user(user_id, username, "Выполнил команду /popular")

    loading_message = await message.answer("🔍 Загружаю популярные игры...")
    log_bot(user_id, "🔍 Загружаю популярные игры...")

    await show_popular_games(loading_message)


@router.callback_query(F.data == "popular_games")
async def popular_games_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username

    log_user(user_id, username, "Нажал на кнопку 'Популярные игры'")
    await callback.answer("Загружаю популярные игры...")

    try:
        await callback.message.delete()
        loading_message = await callback.message.answer("🔍 Загружаю популярные игры...")
        log_bot(user_id, "🔍 Загружаю популярные игры...")
        await show_popular_games(loading_message, original_user_id=user_id, username=username)
    except Exception as e:
        log_error(
            f"Ошибка при отображении сообщения о загрузке популярных игр для пользователя {user_id}: {str(e)}")
        await show_popular_games(callback.message, original_user_id=user_id, username=username)


async def show_popular_games(message, original_user_id=None, username=None):
    user_id = original_user_id or message.from_user.id

    try:
        if user_id:
            log_info(f"Загрузка популярных игр для пользователя {user_id}")
            if username:
                log_user(user_id, username, "Запросил популярные игры")

        games = await rawg_client.get_popular_games(limit=3)

        if not games:
            error_msg = "😔 Не удалось загрузить популярные игры. Попробуйте позже."

            if user_id:
                log_error(
                    f"Не удалось загрузить популярные игры для пользователя {user_id}")

            if hasattr(message, 'edit_text'):
                await message.edit_text(error_msg, reply_markup=get_back_button())
            else:
                await message.answer(error_msg, reply_markup=get_back_button())

            if user_id:
                log_bot(user_id, error_msg)

            return

        game_names = [game.get('name', 'Нет названия') for game in games]

        if user_id:
            log_info(
                f"Загружены популярные игры для пользователя {user_id}: {', '.join(game_names[:3])}")

        result_text = "🔥 Популярные игры на данный момент:\n\n"
        game_ids = []

        for i, game in enumerate(games, 1):
            game_ids.append(game.get('id'))
            name = game.get('name', 'Нет названия')
            rating = game.get('rating', 'N/A')
            released = game.get('released', 'Неизвестно')
            platforms = [platform['platform']['name']
                         for platform in game.get('platforms', [])]
            platforms_text = ', '.join(platforms[:3])
            if len(platforms) > 3:
                platforms_text += f" и еще {len(platforms)-3}"

            tags = []
            for tag in game.get('tags', [])[:3]:
                tags.append(tag.get('name', ''))
            tags_text = ', '.join(tags) if tags else 'Нет тегов'

            result_text += (
                f"{i}. **{name}**\n"
                f"⭐ Рейтинг: {rating}/5\n"
                f"📅 Дата выхода: {released}\n"
                f"🎯 Платформы: {platforms_text}\n"
                f"🏷️ Теги: {tags_text}\n\n"
            )

        first_image = games[0].get('background_image')

        try:
            if hasattr(message, 'delete'):
                await message.delete()

            if first_image:
                await message.answer_photo(
                    photo=first_image,
                    caption=result_text,
                    reply_markup=get_popular_games_menu(game_ids),
                    parse_mode='Markdown'
                )
            else:
                await message.answer(
                    result_text,
                    reply_markup=get_popular_games_menu(game_ids),
                    parse_mode='Markdown'
                )

            if user_id:
                log_bot(user_id, "Отправлен список популярных игр")

        except Exception as e:
            if user_id:
                log_error(
                    f"Ошибка при отображении популярных игр для пользователя {user_id}: {str(e)}")

            await message.answer(
                result_text,
                reply_markup=get_popular_games_menu(game_ids),
                parse_mode='Markdown'
            )

            if user_id:
                log_bot(user_id, "Отправлен список популярных игр (резервный метод)")

    except Exception as e:
        error_text = "Произошла ошибка при загрузке популярных игр. Попробуйте позже."

        if user_id:
            log_error(
                f"Ошибка при загрузке популярных игр для пользователя {user_id}: {str(e)}")

        if hasattr(message, 'edit_text'):
            await message.edit_text(error_text, reply_markup=get_back_button())
        else:
            await message.answer(error_text, reply_markup=get_back_button())

        if user_id:
            log_bot(user_id, error_text)
