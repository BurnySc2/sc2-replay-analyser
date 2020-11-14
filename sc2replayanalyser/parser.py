from typing import Dict, List, Optional, Tuple

import sc2reader
from sc2reader.events.tracker import *
from sc2reader.events.message import *
from sc2reader.events.game import *
from sc2reader.events.base import *
from sc2reader.resources import Replay

import json
from loguru import logger

from .models import *
from .constants import *
from .helper import *


def add_event(
    my_list: List[BuildOrderItem], unit_name: str, start_frame: int, is_upgrade: bool = False, is_action: bool = False
):
    unit_id: int = -1 if is_action else UPGRADE_BY_NAME[unit_name]["id"] if is_upgrade else UNITS_BY_NAME[unit_name][
        "id"
    ]
    event_type: str = (
        "action"
        if is_action
        else "upgrade"
        if is_upgrade
        else "worker"
        if unit_name in WORKERS
        else "structure"
        if UNITS_BY_NAME[unit_name]["is_structure"]
        else "unit"
    )
    my_list.append(BuildOrderItem(unit_name, unit_id, event_type, start_frame, convert_frame_to_time(start_frame),))


def parse_action_events(replay: Replay, player_id: int):
    """
    Looks for all events that are action based:
    Selection of units
    Adding to control groups
    Rightclicking a unit into gas
    Moving a unit out of gas
    Calling down supply
    Salvaging bunker
    Chronoboosting a structure type
    Morphing units and structure commands
    """
    action_events: List[Event] = replay.player[player_id].events
    events: List[BuildOrderItem] = []
    target_unit_command_event = list(filter(lambda x: isinstance(x, TargetUnitCommandEvent), action_events))
    target_points_command_event = list(filter(lambda x: isinstance(x, TargetPointCommandEvent), action_events))
    basic_command_event = list(filter(lambda x: isinstance(x, BasicCommandEvent), action_events))
    for e in action_events:
        if isinstance(e, TargetUnitCommandEvent):
            if e.ability_name == "CalldownMULE":
                # TODO Add call down mule action
                pass
            elif e.ability_name == "ExtraSupplies":
                # TODO Supply drop
                pass
            # TODO Chrono boost structures
            # TODO Inject
        if isinstance(e, TargetPointCommandEvent):
            # TODO Make creep tumor
            pass
        if isinstance(e, BasicCommandEvent):
            if e.ability_name == "SalvageShared":
                # TODO Bunker salvage
                pass
            # TODO Morph archon, morph gate, morph warp gate?

    return events


def parse_tracker_events(replay: Replay, player_id: int):
    """
    Looks for all events where:
    Units are created (some are actions, like MULE)
    Upgrades completed
    Structures started
    Unit types changed (only addons)
    """
    filtered_events: List[Event] = list(
        filter(
            lambda e: e.frame >= 0
            and (
                isinstance(e, (UnitBornEvent, UnitInitEvent))
                and hasattr(e, "control_pid")
                and e.control_pid == player_id
                or isinstance(e, UnitTypeChangeEvent)
                and e.unit.owner.pid == player_id
                or isinstance(e, UpgradeCompleteEvent)
                and e.pid == player_id
            ),
            replay.tracker_events,
        )
    )

    events: List[BuildOrderItem] = []
    events_unhandled = []
    tracked_unit_type_changed: Set[int] = set()

    for e in filtered_events:
        # Worker spawn events
        if isinstance(e, UnitBornEvent) and e.unit.name in WORKERS:
            start_frame = e.frame - UNITS_BY_NAME[e.unit.name]["time"]
            add_event(events, e.unit.name, start_frame)

        # Action events
        elif isinstance(e, UnitBornEvent) and e.unit.name in ACTIONS:
            add_event(events, "call_down_mule", e.frame, is_action=True)

        # Unit spawn events
        elif (
            isinstance(e, UnitBornEvent)
            and e.unit.name in UNITS_BY_NAME
            and not UNITS_BY_NAME[e.unit.name]["is_structure"]
            and e.unit.name not in ACTIONS
        ):
            # If unit has morphs, pick the first name - e.g. WidowMine instead of WidowMineBurrowed
            unit_name = (
                e.unit.type_history[min(e.unit.type_history)].name if hasattr(e.unit, "type_history") else e.unit.name
            )
            start_frame = e.frame - UNITS_BY_NAME[unit_name]["time"]
            add_event(events, unit_name, start_frame)
            # TODO Convert some units into actions, e.g. MULE

        # Gas structure started
        elif isinstance(e, UnitInitEvent) and e.unit.name in GAS_STRUCTURES:
            add_event(events, e.unit.name, e.frame)
            add_workers_to_gas_frame = e.frame + UNITS_BY_NAME[e.unit.name]["time"]
            add_event(events, "3worker_to_gas", add_workers_to_gas_frame, is_action=True)

        # Building started
        elif (
            isinstance(e, UnitInitEvent) and e.unit.name in UNITS_BY_NAME and UNITS_BY_NAME[e.unit.name]["is_structure"]
        ):
            if hasattr(e.unit, "type_history") and e.unit_id not in tracked_unit_type_changed:
                tracked_unit_type_changed.add(e.unit_id)
                previous_type_name: str = ""
                for index, (frame, unit_type) in enumerate(e.unit.type_history.items()):
                    unit_type: UnitType
                    unit_name: str = unit_type.name
                    # Initial unit creation
                    if index == 0:
                        previous_type_name = unit_name
                        add_event(events, unit_name, frame)
                    # Track unit morph history for Orbital and PF
                    elif unit_type.name in ["OrbitalCommand", "PlanetaryFortress"]:
                        # Track OC morphs of new command centers
                        start_frame = frame - UNITS_BY_NAME[unit_name]["time"]
                        add_event(events, unit_name, start_frame)
                        # It may change to OrbitalFlying and then back to OrbitalCommand, so only count OrbitalCommand morph once
                        break
                    # Addon changed: dettach or attachment of addon
                    elif unit_type.name.endswith("TechLab") or unit_type.name.endswith("Reactor"):
                        unit_type: UnitType
                        was_dettach = unit_name in NAKED_ADDONS
                        # Find structure name that attached or dettached from the addon
                        structure_type: str = [
                            production_type
                            for production_type in PRODUCTION_TYPES
                            if production_type in previous_type_name or production_type in unit_name
                        ][0]
                        # Find the addon name
                        addon_type = (
                            "TechLab" if (unit_name in TECHLABS or previous_type_name in TECHLABS) else "Reactor"
                        )
                        if was_dettach:
                            action_name = f"dettach_{structure_type.lower()}_from_{addon_type.lower()}"
                            add_event(
                                events, action_name, frame, is_action=True,
                            )
                        else:
                            action_name = f"attach_{structure_type.lower()}_to_free_{addon_type.lower()}"
                            add_event(
                                events, action_name, frame, is_action=True,
                            )
                        previous_type_name = unit_name

            else:
                unit_name: str = e.unit.name[:-4] if e.unit.name in RICH_GAS_STRUCTURES else e.unit.name
                add_event(events, unit_name, e.frame)

        # Initial structures
        elif (
            isinstance(e, UnitBornEvent)
            and e.unit.name in CCs
            and e.unit_id not in tracked_unit_type_changed
            and e.frame <= 0
            and hasattr(e.unit, "type_history")
        ):
            tracked_unit_type_changed.add(e.unit_id)
            for index, (frame, unit_type) in enumerate(e.unit.type_history.items()):
                unit_type: UnitType
                # if index > 0 and unit_type.name == "OrbitalCommand":
                # Track OC morphs of new command centers
                start_frame = frame - UNITS_BY_NAME[unit_type.name]["time"]
                add_event(events, unit_type.name, start_frame)

        # Upgrade finished
        elif isinstance(e, UpgradeCompleteEvent) and e.upgrade_type_name in UPGRADE_BY_NAME:
            start_frame = e.frame - UPGRADE_BY_NAME[e.upgrade_type_name]["cost"]["time"]
            add_event(events, e.upgrade_type_name, start_frame, is_upgrade=True)
            # events.append((start_frame, "upgrade", e.upgrade_type_name))

        # Ignore events
        elif isinstance(e, UnitBornEvent) and e.unit_type_name in IGNORE_UNIT_BORN_EVENTS:
            # Reaper grenade counts as unit
            logger.info(f"Unhandled event: {type(e)} {convert_frame_to_time(e.frame)} {e.unit.name}")
            pass
        elif isinstance(e, UnitTypeChangeEvent):
            # Supply depot lower, tank siege, liberator siege / unsiege
            logger.info(f"Unhandled event: {type(e)} {convert_frame_to_time(e.frame)} {e.unit.name}")
        elif isinstance(e, UpgradeCompleteEvent) and e.upgrade_type_name in IGNORE_UPGRADE_COMPLETE_EVENTS:
            # Spray events
            pass

        # All other events
        else:
            events_unhandled.append(e)
            if hasattr(e, "unit") and hasattr(e.unit, "name"):
                logger.warning(f"Unhandled event: {type(e)} {convert_frame_to_time(e.frame)} {e.unit.name}")
            elif isinstance(e, UpgradeCompleteEvent):
                logger.warning(f"Unhandled event: {type(e)} {convert_frame_to_time(e.frame)} {e.upgrade_type_name}")
            else:
                logger.warning(f"Unhandled event: {type(e)} {convert_frame_to_time(e.frame)}")

    return events


def parse_addons(events: List[BuildOrderItem], unit_type: UnitType):
    pass
