from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_detail_search_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Поиск игр", callback_data="search_games")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
    ])
    return keyboard 
