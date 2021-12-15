from dataclasses import dataclass


@dataclass
class ShindenPlayer:
    player: str
    quality: str
    audio: str
    subs: str
    upload_date: int
    player_id: int
