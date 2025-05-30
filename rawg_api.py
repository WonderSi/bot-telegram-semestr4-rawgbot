import aiohttp
from config import RAWG_API_KEY, RAWG_BASE_URL
from typing import Dict


class RAWGClient:
    def __init__(self):
        self.api_key = RAWG_API_KEY
        self.base_url = RAWG_BASE_URL

    async def _make_request(self, endpoint: str, params: Dict = None):

        if params is None:
            params = {}
        params['key'] = self.api_key

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/{endpoint}", params=params) as response:
                    if response.status == 200:
                        return await response.join()
                    print(
                        f"HTTP ошибка: {response.status} - {response.reason}")
                    return
            except Exception as e:
                print(f"ОШибка запроса к API", e)
                return None

        async def serach_games(self, query: str, limit: int = 5):
            params = {
                'search': query,
                'page_size': limit,
                'ordering': '-rating'
            }
            data = await self._make_request('games', params)
            return data.get('results', []) if data else []
