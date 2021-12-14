from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Episode:
    id: int
    index: int
    title: Optional[str]
    online: bool
    filler: bool
    languages: List[str]
    airing_date: Optional[int]
