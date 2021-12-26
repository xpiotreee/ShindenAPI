from pydantic.dataclasses import dataclass

from .anime_info.classes import *
from .episodes.classes import *
from .players.classes import *
from .series.classes import *


@dataclass
class Tag:
    type: str
    name: str
    description: str