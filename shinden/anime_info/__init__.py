from aiohttp import ClientSession
from fastapi import HTTPException
from datetime import datetime
from utils.lxml import text, number
from lxml import etree
from .classes import *


class Paths:
    NOT_FOUND = '/html/body/div/div[2]/p[@class=\'enormous-font bree-font\']'
    PLUS18 = '/html/body/div[@id=\'plus18\']'
    NAME = '/html/body/div[2]/div/h1'
    OTHER_TITLES = '/html/body/div[2]/div/div'
    DESCRIPTION = '/html/body/div[2]/div/article/section[1]/div/p'
    IMG = '/html/body/div[2]/div/aside/section[1]/a'
    TAGS_GROUPS = '/html/body/div[2]/div/article/section[1]/table/tbody/tr'
    TAG_GROUP_NAME = './/td'
    TAGS = '/html/body/div[2]/div/article/section[1]/table/tbody/tr[{group_index}]/td/ul/li/a'
    TOTAL_RATING = '/html/body/div[2]/div/aside/section[3]/section/div/div/h3/span'
    RATING_COUNT = '/html/body/div[2]/div/aside/section[3]/section/div/div/span'
    PLOT_RATING = '/html/body/div[2]/div/aside/section[3]/ul/li[1]'
    GRAPHICS_RATING = '/html/body/div[2]/div/aside/section[3]/ul/li[2]'
    MUSIC_RATING = '/html/body/div[2]/div/aside/section[3]/ul/li[3]'
    CHARACTERS_RATING = '/html/body/div[2]/div/aside/section[3]/ul/li[4]'
    INFO = '/html/body/div[2]/div/aside/section[4]/dl/dd/text()'
    STUDIOS = '/html/body/div[2]/div/aside/section[4]/dl/dd/a'
    STATS = '/html/body/div[2]/div/aside/section[5]/dl/dd/text()'


async def get_anime_info(http: ClientSession, anime_id):
    url = f'https://shinden.pl/series/{anime_id}'
    async with http.get(url) as res:
        html = await res.text()
    
    root = etree.HTML(html)

    not_found = root.xpath(Paths.NOT_FOUND)
    if not_found:
        raise HTTPException(status_code=404, detail='Anime not found')
    
    plus18 = root.xpath(Paths.PLUS18)
    if plus18:
        plus18 = plus18[0]
        plus18.getparent().remove(plus18)

    name = text(root, Paths.NAME)[len('Anime: '):]
    other_titles = text(root, Paths.OTHER_TITLES).split(',')
    other_titles = [x.strip() for x in other_titles if x.strip()]
    description = text(root, Paths.DESCRIPTION)
    img_path = root.xpath(Paths.IMG)[0].attrib['href']

    tags = []
    for (i, element) in enumerate(root.xpath(Paths.TAGS_GROUPS)):
        tags_path = Paths.TAGS.format(group_index=i+1)
        tags_elements = element.xpath(tags_path)
        tags.append(TagsGroup(
            name=element.xpath(Paths.TAG_GROUP_NAME)[0].text[:-len(':')],
            tags=[tag.text for tag in tags_elements]
        ))
    
    rating = Rating(
        total=number(text(root, Paths.TOTAL_RATING)),
        count=int(text(root, Paths.RATING_COUNT)[:-len(' głosów')]),
        plot=number(text(root, Paths.PLOT_RATING)),
        graphics=number(text(root, Paths.GRAPHICS_RATING)),
        music=number(text(root, Paths.MUSIC_RATING)),
        characters=number(text(root, Paths.CHARACTERS_RATING))
    )

    info_elements = root.xpath(Paths.INFO)
    studios_elements = root.xpath(Paths.STUDIOS)
    info = Info(
        type=f'{info_elements[0]}',
        status=f'{info_elements[1]}',
        start_airing=datetime.strptime(f'{info_elements[2]}', '%d.%m.%Y').timestamp() * 1000,
        end_airing=datetime.strptime(f'{info_elements[3]}', '%d.%m.%Y').timestamp() * 1000,
        episode_count=int(f'{info_elements[4]}'),
        studios=[studio.text for studio in studios_elements],
        episode_length=int(f'{info_elements[-2]}'[:-len('min')]),
        mpaa=f'{info_elements[-1]}',
    )

    stats_elements = root.xpath(Paths.STATS)
    stats = Stats(
        *[int(f'{element}') for element in stats_elements]
    )

    return AnimeInfo(
        id=anime_id,
        name=name,
        other_titles=other_titles,
        description=description,
        image_url=f'https://shinden.pl{img_path}',
        tags_groups=tags,
        rating=rating,
        info=info,
        stats=stats
    )