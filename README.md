[![Actions Status](https://github.com/BurnySc2/sc2-replay-analyser/workflows/RunTests/badge.svg)](https://github.com/BurnySc2/sc2-replay-analyser/actions)

# SC2 Replay Analyser
Work in progress

A python analyser library to extract StarCraft II build orders (for now).

# Installation
```
pip install poetry
poetry install
```

Run with 
```
poetry run python main.py
```

# Replay Analysis
### Disclaimer
For units and upgrades, they will only show up in the parsed list of events, if they finished within the replay.
That means if you start `Stimpack` research but end the game while `Stimpack` has not been finished researching, it will not show up in the list.
### Example: Extract build order
TODO

# Development
## Run Tests
Run all tests

`poetry run pytest test/`

# TODO Features

## Macro analysis
### All races
- How long supply blocked
### Terran
- CC count
- Production count
- How long CCs were idle (not making SCVs)
- How long production was idle (not making units)
- How long ebays were idle after they finished constructing
- How much was armoy delayed/late for 2-2
- Extract important timings: Upgrade finished
- Graphs: 
    - worker supply
    - army supply
    - total supply
    - money in bank
    - amount of free supply (max supply) 
    - used supply
- Comparison between 2 (or more) replays: example / ideal build


