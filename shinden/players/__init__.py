from aiohttp import ClientSession
from datetime import datetime
from lxml import etree
from .classes import *
import asyncio
import json

class Paths:
    ELEMENTS = '//tbody/tr/td/a'
    PLUS18 = '/html/body/div[@id=\'plus18\']'


async def get_players(http: ClientSession, episode_id):
    async with http.get(f'https://shinden.pl/episode/1/view/{episode_id}') as res:
        html = await res.text()
    
    root = etree.HTML(html)
    players = []

    plus18 = root.xpath(Paths.PLUS18)
    if plus18:
        plus18 = plus18[0]
        plus18.getparent().remove(plus18)
    
    elements = root.xpath(Paths.ELEMENTS)

    for element in elements:
        info = element.attrib.get('data-episode', None)
        if info is None:
            continue

        info = json.loads(info)
        players.append(
            ShindenPlayer(
                player=info['player'],
                quality=info['max_res'],
                audio=info['lang_audio'],
                subs=info['lang_subs'],
                upload_date=int(datetime.strptime(info['added'], '%Y-%m-%d %H:%M:%S').timestamp() * 1000),
                player_id=int(info['online_id'])
            )
        )
    
    return players

async def get_player(shinden, player_id):
    async with shinden._http.get(f'https://api4.shinden.pl/xhr/{player_id}/player_load',
        params={
            'auth': shinden.api_auth
        }
    ) as res:
        time = int(await res.text())
    
    await asyncio.sleep(time)

    async with shinden._http.get(f'https://api4.shinden.pl/xhr/{player_id}/player_show',
        params={
            'auth': shinden.api_auth
        }    
    ) as res:
        html = await res.text()
    
    for line in html.split('\n'):
        if 'iframe' in line:
            return line
