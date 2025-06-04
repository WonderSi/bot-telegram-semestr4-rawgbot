from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_search_type_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 По названию", callback_data="search_by_name"),
            InlineKeyboardButton(text="🎭 По жанру", callback_data="search_by_genre")
        ],
        [
            InlineKeyboardButton(text="🏷️ По тегам", callback_data="search_by_tag"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
        ]
    ])
    return keyboard 
