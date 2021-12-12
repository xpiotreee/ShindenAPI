from aiohttp import ClientSession
from utils.lxml import text, number, text_builder
from lxml import etree
from .classes import *


class Paths:
    SEARCH_RESULTS = '/html/body/div[2]/div/section[2]/section/article/ul[@class=\'div-row\']'
    NAME = './/li[@class=\'desc-col\']/h3/a'
    TAGS = './/li[@class=\'desc-col\']/ul/li/a'
    STATUS = './/li[@class=\'title-status-col\']'
    TYPE = './/li[@class=\'title-kind-col\']'
    EPISODE_COUNT = './/li[@class=\'episodes-col\']'
    RATING_ELEMENT = './/li[@class=\'ratings-col\']'
    TOTAL_RATING = './/div[@data-type=\'total\']/span/text()'
    PLOT_RATING = './/div[@data-type=\'story\']/span/text()'
    GRAPHICS_RATING = './/div[@data-type=\'graphics\']/span/text()'
    MUSIC_RATING = './/div[@data-type=\'music\']/span/text()'
    CHARACTERS_RATING = './/div[@data-type=\'titlecahracters\']/span/text()'
    RATING_TOP = './/li[@class=\'rate-top\']/text()'
    THUMBNAIL = './/li[@class=\'cover-col\']/a'


async def search(http: ClientSession, query, page=1):
    params = {
        'search': query
    }

    if page > 1:
        params['page'] = page

    async with http.get('https://shinden.pl/series', params=params) as res:
        html = await res.text()
        f = open('debug.html', 'w')
        f.write(html)
        f.close()
    
    root = etree.HTML(html)
    results = []

    elements = root.xpath(Paths.SEARCH_RESULTS)
    for element in elements:
        id = int(element.xpath(Paths.NAME)[0].attrib['href'][len('/series/'):].split('-')[0])
        name = text_builder(element.xpath(Paths.NAME)[0])
        type = text(element, Paths.TYPE)

        episodes_count = text(element, Paths.EPISODE_COUNT)
        if episodes_count and episodes_count.strip():
            episodes_count = int(episodes_count)
        else:
            episodes_count = 0

        status = text(element, Paths.STATUS)
        tags = [tag.text for tag in element.xpath(Paths.TAGS)]

        rating_element = element.xpath(Paths.RATING_ELEMENT)[0]
        if list(rating_element):            
            rating = SearchResultRating(
                total=number(rating_element.xpath(Paths.TOTAL_RATING)),
                plot=number(rating_element.xpath(Paths.PLOT_RATING)),
                graphics=number(rating_element.xpath(Paths.GRAPHICS_RATING)),
                music=number(rating_element.xpath(Paths.MUSIC_RATING)),
                characters=number(rating_element.xpath(Paths.CHARACTERS_RATING)),
                top=number(element.xpath(Paths.RATING_TOP))
            )
        else:
            rating = None

        thumbnail = element.xpath(Paths.THUMBNAIL)[0]
        if thumbnail.attrib['href'] == 'javascript:void(0)':
            print(thumbnail.attrib['style'])
            thumbnail_path = thumbnail.attrib['style'][len('background-image: url('):-len(')')]
        else:
            thumbnail_path = thumbnail.attrib['href']


        results.append(
            SearchResult(
                id=id,
                name=name,
                type=type,
                episodes_count=episodes_count,
                status=status,
                tags=tags,
                rating=rating,
                thumbnail_url=f'https://shinden.pl{thumbnail_path}'
            )
        )

    return results
