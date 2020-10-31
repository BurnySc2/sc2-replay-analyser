from typing import Dict, List, Optional, Tuple

import sc2reader
from sc2reader.events.tracker import *
from sc2reader.events.message import *
from sc2reader.events.game import *
from sc2reader.events.base import *
from sc2reader.resources import Replay

import json
from loguru import logger

# from .models import *
# from .constants import *
# from .helper import *
from sc2replayanalyser.parser import *


import zlib
import base64
from pathlib import Path

custom_actions_json_path = Path(__file__).parent / "sc2planner_customactions.json"
with custom_actions_json_path.open() as f:
    data = json.load(f)
# CUSTOMACTIONS_BY_NAME = {}
# for entry in data:
#     CUSTOMACTIONS_BY_NAME[entry["internal_name"]] = entry
CUSTOMACTIONS_BY_NAME: Dict[str, Dict[str, str]] = {entry["internal_name"]: entry for entry in data}


def create_link(race, build_order: List[BuildOrderItem]):
    url_list = ["https://burnysc2.github.io/sc2-planner?", f"race={race}", "&bo=002"]
    # Each item is in form of: {id: int, type: str}
    compact_bo: list = []

    for item in build_order:
        if item.type == "action":
            action = CUSTOMACTIONS_BY_NAME[item.name]
            compact_bo.append({"id": action["id"], "type": item.type})
        elif item.type in ["worker", "unit", "structure"]:
            unit = UNITS_BY_NAME[item.name]
            compact_bo.append({"id": unit["id"], "type": item.type})
        elif item.type == "upgrade":
            upgrade = UPGRADE_BY_NAME[item.name]
            compact_bo.append({"id": upgrade["id"], "type": item.type})

    b64_string = encode_b64(compact_bo)
    print("002" + b64_string)
    url_list.append(b64_string)
    return "".join(url_list)


def encode_b64(build_order: list) -> str:
    json_string = json.dumps(build_order, separators=(",", ":"))
    zlib_compressed = zlib.compress(json_string.encode())
    zlib_b64 = base64.b64encode(zlib_compressed)
    return zlib_b64.decode()


def decode_b64(encoded_bo: str) -> list:
    zlib_compressed = base64.b64decode(encoded_bo.encode())
    json_string = zlib.decompress(zlib_compressed).decode()
    build_order = json.loads(json_string)
    return build_order


# TODO Write as test
if __name__ == "__main__":
    # Example with a depot
    bo = [{"id": 19, "type": "structure"}]
    encoded = encode_b64(bo)
    encoded_from_javascript = "eJyLrlbKTFGyMrTUUSqpLEhVslIqLikqTS4pLUpVqo0FAJE9Cgc="
    assert encoded == encoded_from_javascript
    decoded = decode_b64(encoded)
    assert bo == decoded
