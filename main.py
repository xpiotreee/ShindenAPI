from typing import Optional
from fastapi import FastAPI
from shinden import Shinden

app = FastAPI()
shinden = Shinden()

@app.on_event('startup')
async def startup_event():
    await shinden.init()


@app.get('/')
def read_root():
    return 'chej'


@app.get('/anime/{anime_id}')
async def anime_info(anime_id: str):
    return await shinden.get_anime_info(anime_id)
