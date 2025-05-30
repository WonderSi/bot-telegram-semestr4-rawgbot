from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Поиск игр", callback_data="search_games")],
        [InlineKeyboardButton(text="🔥 Популярные игры", callback_data="popular_games")],
        [InlineKeyboardButton(text="🎲 Случайная игра", callback_data="random_game")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])
    return keyboard
