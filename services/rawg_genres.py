from typing import Dict, List
from services.rawg_client import RAWGClient

class RAWGGenresService(RAWGClient):
    def __init__(self):
        super().__init__()
        
    async def get_genres(self) -> List[Dict]:
        data = await self._make_request('genres')
        return data.get('results', []) if data else []
        
    async def get_tags(self, limit: int = 20) -> List[Dict]:
        params = {
            'page_size': limit
        }
        data = await self._make_request('tags', params)
        return data.get('results', []) if data else [] 