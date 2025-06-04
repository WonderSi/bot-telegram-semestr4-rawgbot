from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_random_game_menu(game_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Подробнее", callback_data=f"details_random_{game_id}"),
            InlineKeyboardButton(text="🔄 Еще", callback_data="random_game")
        ],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
    ])
    return keyboard

def get_detail_random_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_random")],
        [InlineKeyboardButton(text="🎲 Еще случайная игра", callback_data="random_game")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
    ])
    return keyboard 
