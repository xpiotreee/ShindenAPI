from typing import Optional
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from shinden import Shinden
from shinden.anime_info.classes import AnimeInfo
from shinden.players.classes import ShindenPlayer
from shinden.series.classes import SearchResult
from shinden.episodes.classes import Episode
from typing import List, Optional


app = FastAPI()
shinden = Shinden()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def startup_event():
    await shinden.init()


@app.get('/')
def read_root():
    return 'chej'


@app.get('/series/{anime_id}', response_model=AnimeInfo)
async def anime_info(anime_id: int):
    return await shinden.get_anime_info(anime_id)


@app.get('/series/{anime_id}/episodes', response_model=List[Episode])
async def episodes(anime_id: int):
    return await shinden.get_episodes(anime_id)


@app.get('/players/{episode_id}', response_model=List[ShindenPlayer])
async def players(episode_id: int):
    return await shinden.get_players(episode_id)


@app.get('/player/{player_id}', response_model=str)
async def player(player_id: int):
    iframe_str = await shinden.get_player(player_id)
    return Response(content=iframe_str, media_type='text/html; charset=utf-8')


@app.get('/series/', response_model=List[SearchResult])
async def search(q: Optional[str] = None, page: Optional[int] = 1):
    return await shinden.series(q, page)
