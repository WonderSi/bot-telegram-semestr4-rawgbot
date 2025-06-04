import aiohttp
from typing import Dict, Optional
from config import RAWG_API_KEY, RAWG_BASE_URL

class RAWGClient:
    def __init__(self):
        self.api_key = RAWG_API_KEY
        self.base_url = RAWG_BASE_URL
        self.excluded_tags = [
            'nudity', 
            'sexual-content', 
            'gore',
            'violent', 
            'mature', 
            'adult',
            'nsfw',
            'horror',
            'sexual',
            'blood',
            'violence',
            'drugs',
            'explicit',
            'erotic',
            'gambling'
        ]

    async def _make_request(self, endpoint: str, params: Dict = None, user_id: Optional[int] = None):
        if params is None:
            params = {}
        params['key'] = self.api_key
        
        if 'exclude_tags' not in params:
            params['exclude_tags'] = ','.join(self.excluded_tags)
            
        if 'exclude_additions' not in params and endpoint == 'games':
            params['exclude_additions'] = 'true'
            
        if 'esrb' not in params and endpoint == 'games':
            params['esrb'] = '1,2,3'

        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                
                return data
