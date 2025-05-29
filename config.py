import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAWG_API_KEY = os.getenv('RAWG_API_KEY')
RAWG_URL = 'https://api.rawg.io/api'
