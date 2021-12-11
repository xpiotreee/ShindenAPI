from dataclasses import dataclass
from typing import List


@dataclass
class TagsGroup:
    name: str
    tags: List[str]


@dataclass
class Rating:
    total: float
    count: int
    plot: float
    graphics: float
    music: float
    characters: float
    

@dataclass
class Info:
    type: str
    status: str
    start_airing: str
    end_airing: str
    episode_count: int
    studios: List[str]
    episode_length: str
    mpaa: str


@dataclass
class Stats:
    watching: int
    watched: int
    skipped: int
    paused: int
    dropped: int
    planning: int
    liked: int


@dataclass
class AnimeInfo:
    id: str
    name: str
    other_titles: List[str]
    description: str
    image_url: str
    tags_groups: List[TagsGroup]
    rating: Rating
    info: Info
    stats: Stats