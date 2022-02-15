import json
from aiohttp import ClientSession
from lxml import etree
from . import anime_info
from . import series
from . import episodes
from . import players

class Shinden():
    def __init__(self):
        self._http = None
        self.api_auth = ''
        self.tags = ''
    
    async def init(self):
        self._http = ClientSession(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36.',
                'Accept-Language': 'pl'
            }
        )

        async with self._http.get(f'https://shinden.pl/') as res:
            html = await res.text()
        
        root = etree.HTML(html)
        script = root.xpath('//script[contains(text(),\'var safe = true;\')]/text()')[0]
        script = f'{script}'
        for line in script.split('\n'):
            if '_Storage.basic =' not in line:
                continue

            self.api_auth = line[line.find('\'') + 1:line.rfind('\'')]
        
        f = open('tags.json', 'r')
        self.tags = f.read()
        f.close()
    
    async def get_anime_info(self, anime_id):
        return await anime_info.get_anime_info(self._http, anime_id)
    
    async def get_episodes(self, anime_id):
        return await episodes.get_episodes(self._http, anime_id)
    
    async def get_players(self, episode_id):
        return await players.get_players(self._http, episode_id)
    
    async def get_player(self, player_id):
        return await players.get_player(self, player_id)
    
    async def series(self, search, page, genres, sort_by, sort_order):
        return await series.series(self._http, search, page, genres, sort_by, sort_order)