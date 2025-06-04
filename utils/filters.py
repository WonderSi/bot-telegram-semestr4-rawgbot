from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class CallbackDataEquals(BaseFilter):
    
    def __init__(self, value: str):
        self.value = value
        
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == self.value

class CallbackDataStartsWith(BaseFilter):
    
    def __init__(self, prefix: str):
        self.prefix = prefix
        
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith(self.prefix) 
