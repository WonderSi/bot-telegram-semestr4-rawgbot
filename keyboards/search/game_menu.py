from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_game_menu(game_id: int, query: str, current_index: int, total_games: int, search_type: str = 'name'):
    first_row = [InlineKeyboardButton(text="📋 Подробнее", callback_data=f"details_{game_id}")]

    if current_index + 1 < total_games:
        first_row.append(InlineKeyboardButton(text="🔄 Еще", callback_data=f"search_next_{query}_{current_index}_{total_games}_{search_type}"))

    buttons = [
        first_row,
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard 
