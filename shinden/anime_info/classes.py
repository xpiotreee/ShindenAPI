from pydantic.dataclasses import dataclass 
from typing import List


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
    start_airing: int
    end_airing: int
    episode_count: int
    studios: List[str]
    episode_length: int
    mpaa: str


@dataclass
class Stats:
    watching: int = 0
    watched: int = 0
    skipped: int = 0
    paused: int = 0
    dropped: int = 0
    planning: int = 0
    liked: int = 0


@dataclass
class AnimeInfo:
    id: int
    name: str
    other_titles: List[str]
    description: str
    image_url: str
    tags: List[str]
    rating: Rating
    info: Info
    stats: Stats
