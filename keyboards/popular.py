from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_popular_games_menu(game_ids: list):
    buttons = []
    for i, game_id in enumerate(game_ids):
        buttons.append([InlineKeyboardButton(
            text=f"📋 Подробнее об игре {i+1}", callback_data=f"details_popular_{game_id}")])

    buttons.append([InlineKeyboardButton(
        text="🏠 Главное меню", callback_data="back_to_menu")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_detail_popular_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="◀️ Назад к популярным играм", callback_data="popular_games")],
        [InlineKeyboardButton(text="🏠 Главное меню",
                              callback_data="back_to_menu")]
    ])
    return keyboard
