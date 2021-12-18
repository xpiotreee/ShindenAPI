from aiohttp import ClientSession
from datetime import datetime
from utils.lxml import text
from lxml import etree
from .classes import *


class Paths:
    PLUS18 = '/html/body/div[@id=\'plus18\']'
    LIST = '//tbody[1]/tr'
    INDEX = './/td[1]'
    TITLE = './/td[@class=\'ep-title\']'
    ONLINE = './/td/i[@class=\'fa fa-fw fa-check\']'
    FILLER = './/td/i[@title=\'Filler\']'
    LANGUAGES = './/td[4]/span'
    AIRING_DATE = './/td[@class=\'ep-date\']'
    INFO = './/td[@class=\'button-group\']/a'



async def get_episodes(http: ClientSession, anime_id):
    async with http.get(f'https://shinden.pl/series/{anime_id}/all-episodes') as res:
        html = await res.text()
    
    
    root = etree.HTML(html)
    episodes = []

    plus18 = root.xpath(Paths.PLUS18)
    if plus18:
        plus18 = plus18[0]
        plus18.getparent().remove(plus18)

    episodes_list = root.xpath(Paths.LIST)
    for element in episodes_list:
        id = int(element.xpath(Paths.INFO)[0].attrib['href'].split('/')[-1])

        languages = []
        for language in element.xpath(Paths.LANGUAGES):
            languages.append(
                language.attrib['class'].split('-')[-1]
            )
        
        airing_date_str = text(element, Paths.AIRING_DATE)
        if airing_date_str:
            airing_date = int(datetime.strptime(
                text(element, Paths.AIRING_DATE), '%Y-%m-%d'
            ).timestamp() * 1000)
        else:
            airing_date = None

        episodes.append(Episode(
            id=id,
            index=int(text(element, Paths.INDEX)),
            title=text(element, Paths.TITLE),
            online=len(element.xpath(Paths.ONLINE)) == 1,
            filler=len(element.xpath(Paths.FILLER)) == 1,
            languages=languages,
            airing_date=airing_date
        ))
    
    episodes.reverse()
    return episodes
