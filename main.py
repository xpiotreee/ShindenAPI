from typing import Optional
from fastapi import FastAPI
from shinden import Shinden
from shinden.anime_info.classes import AnimeInfo
from shinden.search.classes import SearchResult
from typing import List, Optional


app = FastAPI()
shinden = Shinden()

@app.on_event('startup')
async def startup_event():
    await shinden.init()


@app.get('/')
def read_root():
    return 'chej'


@app.get('/anime/{anime_id}', response_model=AnimeInfo)
async def anime_info(anime_id: int):
    return await shinden.get_anime_info(anime_id)


@app.get('/search/', response_model=List[SearchResult])
async def search(q: str, page: Optional[int] = 1):
    return await shinden.search(q, page)