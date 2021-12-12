from aiohttp import ClientSession
from . import anime_info
from . import search

class Shinden():
    def __init__(self):
        self._http = None
    
    async def init(self):
        self._http = ClientSession(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36.',
                'Accept-Language': 'pl,en-US;q=0.9,en;q=0.8'
            }
        )
    
    async def get_anime_info(self, anime_id):
        return await anime_info.get_anime_info(self._http, anime_id)
    
    async def search(self, query, page=1):
        return await search.search(self._http, query, page)