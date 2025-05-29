import aiohttp
from config import RAWG_API_KEY, RAWG_BASE_URL


class RAWGClient:
    def __init__(self):
        self.api_key = RAWG_API_KEY
        self.base_url = RAWG_BASE_URL

    
