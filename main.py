# Other
import time
import os
import sys
import re
import time
import json
from contextlib import contextmanager
from pathlib import Path
from dataclasses import dataclass

# https://pypi.org/project/dataclasses-json/#description
from dataclasses_json import DataClassJsonMixin

# Coroutines and multiprocessing
import asyncio
import aiohttp
from multiprocessing import Process, Lock, Pool

# Simple logging https://github.com/Delgan/loguru
from loguru import logger

# Database
import sqlite3

# Remove previous default handlers2
logger.remove()
# Log to console
logger.add(sys.stdout, level="INFO")
# Log to file, max size 1 mb
logger.add("main.log", rotation="1 MB", retention="7 days", level="INFO")

# Type annotation / hints
from typing import List, Iterable, Union, Set

import sc2reader
from sc2reader.events.tracker import *
from sc2reader.events.message import *
from sc2reader.events.game import *
from sc2reader.data import *
from sc2reader.resources import Replay

from sc2replayanalyser.parser import parse_tracker_events, parse_action_events
from sc2replayanalyser.sc2planner import create_link


async def main():  # Release version and game length info. Nothing else
    replay_path = Path(__file__).parent / "test" / "replays" / "TvP Uthermal 2mine drop into 2 tank push.SC2Replay"

    # Also loads players and chat events:
    # replay = sc2reader.load_replay(str(replay_path), load_level=2)

    # Also loads game events:
    replay: Replay = sc2reader.load_replay(str(replay_path), load_level=4)
    my_action_events = parse_action_events(replay, 1)
    my_events = parse_tracker_events(replay, 1)

    # All events include units and structures from the start of the game
    all_events = my_action_events + my_events
    all_events.sort(key=lambda k: k.frame)

    # Exclude workers or structures that spawned at frame 0, since they are not part of the build order
    shortened = list(filter(lambda x: 0 < x.frame < 22.4 * 5 * 60 + 0, all_events))
    link = create_link("terran", shortened)
    # "002eJyLrlbKTFGyMjHVUSqpLEhVslIqzy/KTi1Sqo0FAHMmCK8="
    # link = create_link("terran", all_events)
    print(link)
    print()


if __name__ == "__main__":
    asyncio.run(main())
