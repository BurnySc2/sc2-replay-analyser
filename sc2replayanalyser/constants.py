from typing import Set, Dict, List
from pathlib import Path
import json

# ADDON_LOOKUP = {
#     "BuildBarracksTechlab": 60,
#     "BuildBarracksReactor": 61,
#     "BuildFactoryTechlab": 62,
#     "BuildFactoryRector": 63,
#     "BuildStarportTechlab": 64,
#     "BuildStarportReactor": 65,
# }

WORKERS = {"SCV", "Drone", "Probe"}

GAS_STRUCTURES: Set[str] = {"Extractor", "Refinery", "Assimilator"}

TECHLABS: Set[str] = {"BarracksTechLab", "FactoryTechLab", "StarportTechLab"}
REACTORS: Set[str] = {"BarracksReactor", "FactoryReactor", "StarportReactor"}
ADDONS: Set[str] = TECHLABS | REACTORS
BARRACKS_ADDONS: Set[str] = {addon for addon in ADDONS if addon.startswith("Barracks")}
FACTORY_ADDONS: Set[str] = {addon for addon in ADDONS if addon.startswith("Factory")}
STARPORT_ADDONS: Set[str] = {addon for addon in ADDONS if addon.startswith("Starport")}
NAKED_ADDONS: Set[str] = {"TechLab", "Reactor"}
PRODUCTION_TYPES: List[str] = ["Barracks", "Factory", "Starport"]

CCs = ["CommandCenter", "OrbitalCommand", "PlanetaryFortress"]
RICH_GAS_STRUCTURES = ["RefineryRich", "ExtractorRich", "AssimilatorRich"]

# All the actions that are allowed on sc2planner, e.g. inject, mule, chrono
# ALLOWED_ABILITIES = {
#     # Protoss
#     "ChronoBoostEnergyCost",
#     "UpgradeToWarpGate",
#     "MorphBackToGateway",
#     "ArchonWarp",
#     # Terran
#     "CalldownMULE",
#     # "SalvageShared",
#     # Zerg
#     "CreepTumorBurrowedBuild",
#     "INJECT",
# }

IGNORE_UNIT_BORN_EVENTS = {"KD8Charge"}
IGNORE_UPGRADE_COMPLETE_EVENTS = {"SprayTerran"}

# CC to Orbital etc
ALLOWED_STRUCTURE_TYPE_CHANGES = {
    "OrbitalCommand",
    "PlanetaryFortress",
}

ACTIONS: Set[str] = {
    "MULE",
    "3worker_to_gas",
}


data_json_path = Path(__file__).parent / "data.json"
with data_json_path.open() as f:
    data = json.load(f)
UNITS_BY_NAME = {unit["name"]: unit for unit in data["Unit"]}
UPGRADE_BY_NAME = {upgrade["name"]: upgrade for upgrade in data["Upgrade"]}
