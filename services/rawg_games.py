import random
from services.rawg_client import RAWGClient

class RAWGGamesService(RAWGClient):
    def __init__(self):
        super().__init__()
        
    async def search_games(self, query: str, limit: int = 10, search_type: str = 'name'):
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
        
        data = await self._make_request('games', params)
        return data.get('results', []) if data else []
        
    def get_genre_ids(self):
        return {
            'action': 4,
            'indie': 51,
            'adventure': 3,
            'rpg': 5,
            'strategy': 10,
            'shooter': 2,
            'casual': 40,
            'simulation': 14,
            'puzzle': 7,
            'arcade': 11,
            'platformer': 83,
            'racing': 1,
            'sports': 15,
            'fighting': 6,
            'family': 19,
            'board-games': 28,
            'educational': 34,
            'card': 17,
            'massively-multiplayer': 59,
            'action-adventure': 25,
            'action-rpg': 24,
            'visual-novel': 57,
            'tactical': 160,
            'turn-based': 101,
            'beat-em-up': 143,
            'rogue-like': 639,
            'hack-and-slash': 68,
            'survival': 63,
            'stealth': 69,
            'point-and-click': 2,
            'moba': 36,
            'pinball': 107,
            'party': 138,
            'trivia': 39,
            'chess': 53
        }

    async def get_game_details(self, game_id: int):
        return await self._make_request(f'games/{game_id}')
        
    async def get_game_tags(self, game_id: int):
        data = await self._make_request(f'games/{game_id}')
        if not data:
            return []
        
        return [tag['name'] for tag in data.get('tags', [])]

    async def get_popular_games(self, limit: int = 5):
        params = {
            'ordering': '-rating',
            'page_size': limit,
            'metacritic': '80,100',
        }
        data = await self._make_request('games', params)
        return data.get('results', []) if data else []

    async def get_random_game(self):
        random_page = random.randint(1, 10)
        
        params = {
            'page': random_page,
            'page_size': 20,
            'metacritic': '70,100',
        }
        
        data = await self._make_request('games', params)
        results = data.get('results', []) if data else []
        
        if not results:
            return None
            
        return random.choice(results) 
