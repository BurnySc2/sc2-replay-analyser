from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

from sc2reader.events.tracker import *
from sc2reader.events.message import *
from sc2reader.events.game import *
from sc2reader.events.base import *
from sc2reader.data import *

# https://pypi.org/project/dataclasses-json/#description
from dataclasses_json import DataClassJsonMixin

from .constants import *


class MyRace(Enum):
    Unknown = 0
    Protoss = 1
    Terran = 2
    Zerg = 3


class MyResult(Enum):
    Unknown = 0
    Win = 1
    Loss = 2
    Tie = 3


class MyRegion(Enum):
    Unknown = 0
    US = 1
    EU = 2
    KR = 3


@dataclass
class MyMap(DataClassJsonMixin):
    map_name: str


@dataclass
class MyPlayer(DataClassJsonMixin):
    # .name
    name: str
    # .clan_tag
    clan_tag: str
    # .play_race: "Protoss", "Terran",
    race: str
    # .result: "Win", "Loss"
    result: str
    # .url
    url: str
    # init_data.scaled_rating
    mmr: int

    def __post_init__(self):
        pass


@dataclass
class BuildOrderItem(DataClassJsonMixin):
    name: str
    # The id  of the unit
    id: int
    # One of: ["worker", "structure", "unit", "upgrade", "action"]
    type: str
    # When the creation process started
    frame: int
    # frame / 22.4
    time: str
    # Which unit tag created this unit / structure / upgrade
    created_by: Optional[int] = None
    # When the creation process finishes
    finished_frame: Optional[int] = None

    def __post_init__(self):
        if self.type in {"worker", "unit", "structure"}:
            self.finished_frame = self.frame + UNITS_BY_NAME[self.name]["time"]
        elif self.type in {"upgrade"}:
            self.finished_frame = self.frame + UPGRADE_BY_NAME[self.name]["cost"]["time"]
