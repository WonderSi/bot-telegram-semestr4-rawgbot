import random
from typing import Dict, List, Optional
from services.rawg_client import RAWGClient

class RAWGGamesService(RAWGClient):
    def __init__(self):
        super().__init__()
        
    async def search_games(self, query: str, limit: int = 10, search_type: str = 'name', user_id: int = None):
        params = {
            'page_size': limit,
        }
        
        if search_type == 'name':
            params['search'] = query
        elif search_type == 'genre':
            genre_id = None
            query_lower = query.lower()
            
            if query_lower in self.get_genre_ids():
                genre_id = self.get_genre_ids()[query_lower]
            else:
                for genre_name, genre_id_value in self.get_genre_ids().items():
                    if genre_name in query_lower or query_lower in genre_name:
                        genre_id = genre_id_value
                        break
            
            if genre_id:
                params['genres'] = genre_id
            else:
                params['genres'] = query
        elif search_type == 'tag':
            params['tags'] = query
            params['search_exact'] = 'true'
        
        data = await self._make_request('games', params, user_id)
        return data.get('results', []) if data else []
        
    def get_genre_ids(self):
        return {
            'action': 4,
            'strategy': 10,
            'rpg': 5,
            'shooter': 2,
            'adventure': 3,
            'puzzle': 7,
            'racing': 1,
            'sports': 15,
            'platformer': 83
        }

    async def get_game_details(self, game_id: int, user_id: int = None):
        return await self._make_request(f'games/{game_id}', user_id=user_id)
        
    async def get_game_tags(self, game_id: int, user_id: int = None) -> List[str]:
        data = await self._make_request(f'games/{game_id}', user_id=user_id)
        if not data:
            return []
        
        return [tag['name'] for tag in data.get('tags', [])]

    async def get_popular_games(self, limit: int = 5, user_id: int = None):
        params = {
            'ordering': '-rating',
            'page_size': limit,
            'metacritic': '80,100',
        }
        data = await self._make_request('games', params, user_id)
        return data.get('results', []) if data else []

    async def get_random_game(self, user_id: int = None):
        random_page = random.randint(1, 10)
        
        params = {
            'page': random_page,
            'page_size': 20,
            'metacritic': '70,100',
        }
        
        data = await self._make_request('games', params, user_id)
        results = data.get('results', []) if data else []
        
        if not results:
            return None
            
        return random.choice(results) 
