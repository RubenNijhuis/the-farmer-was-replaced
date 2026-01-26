# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of automation scripts for **The Farmer Was Replaced** (TFWR), a game where you program drones to automate farming tasks. The scripts are written in a Python-like language with game-specific built-ins.

## Running Scripts

Scripts are executed directly within the TFWR game. To run a script:
1. Open the game and load the save
2. Select the script file in the game's code editor
3. Run the script using the game's execution controls

## Language Limitations

The scripting language is Python-like but **not actual Python**:
- **No classes** - only functions and basic types
- **No try/except** - no exception handling
- **No list comprehensions** - use for loops instead
- **No lambda** - define named functions
- **No standard library** - only game built-ins
- **Comments**: Use `#` only, not `"""`docstrings
- `__builtins__.py` contains type stubs for IDE support only (not executed by the game)

## Architecture

### Conventions
- **Area tuple**: Functions use `area = (pos, size)` where `pos = (x, y)` and `size = (width, height)`
- **Max 2 params**: Functions take at most 2 positional params. Extra config uses `options` dict.
- Example: `run_func(area, func, options)` where `options = {"slices": [...], "threaded": True}`

### Entry Point
`main.py` has two modes:
- **Test mode** (`MODE = "test"`): Farm a single crop continuously. Set `TEST_CROP` to choose crop.
- **Target mode** (`MODE = "target"`): Farm resources for a specific unlock.

### Core Systems

**Multi-drone parallelization** (`multi.py`):
- `run_func(area, func, options)` - Single pass with parallel drones
- `run_func_until(area, func, options)` - Loops until `options["should_stop"]()` returns True
- `run_func_looped(area, func)` - Loops forever (no respawn overhead)

**Plot management** (`plot_management.py`):
- `auto_plotter(area, amount_wanted)` - Farms items until target amounts using each module's `farm()` function

**Movement** (`movement.py`):
- `go_to(pos)` - Navigates to coordinates using shortest path (handles world wrapping)

**Crop handling** (`crops.py`):
- `plant_crop(crop)` - Handles soil preparation, watering, and planting

### Crop-Specific Modules
Each crop module has:
- `plant_field(area)` - Plants/grows only (no harvest)
- `farm_field(area)` - Full cycle including harvest (pumpkins, cactus only)
- `farm(area, amount)` - Farm until target amount reached. Auto-selects parallel (if Megafarm unlocked) or single-threaded.

| Module | Notes |
|--------|-------|
| `hay.py`, `carrots.py`, `sunflowers.py`, `dinosaurs.py` | Simple plant and harvest in one pass |
| `trees.py`, `weird_substance.py` | Checkerboard pattern planting |
| `pumpkins.py` | Waits for all to grow, then harvests merged group |
| `cactus.py` | Plants, sorts rows+columns, then harvests chain |
| `gold.py` | Maze farming with wall-following algorithms (ignores area param) |

### Utilities
- `coordinates.py` - `generate_coords(area, mode)` for area traversal
- `utils.py` - `map_over_area(area, func)`, `create_slices(area, options)`
- `cost_calculator.py` - `calculate_remaining_cost(unlock)` returns items still needed (subtracts inventory)
- `hats.py` - Visual feedback via drone hats

## Key Game Concepts

- **Tick costs**: Heavy operations (move, harvest, plant, swap) = 200 ticks; sensing (measure, get_entity_type) = 1 tick
- **World coordinates**: X increases East, Y increases North, origin at (0,0) in Southwest corner
- **Pumpkins**: Merge when adjacent and grown (yield = count³)
- **Cacti**: Chain-harvest when sorted ascending (yield = count²). Sort rows then columns to create gradient from (0,0) to (max,max)
- **Mazes**: Created with `use_item(Items.Weird_Substance)` on a bush
