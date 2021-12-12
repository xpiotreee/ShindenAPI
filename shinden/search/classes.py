from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SearchResultRating:
    total: float = 0
    plot: float = 0
    graphics: float = 0
    music: float = 0
    characters: float = 0
    top: float = 0


@dataclass
class SearchResult:
    id: int
    name: str
    type: str
    episodes_count: int
    status: str
    tags: List[str]
    thumbnail_url: str
    rating: Optional[SearchResultRating] = None
