# The Farmer Was Replaced - Automation Scripts

A collection of automation scripts for **The Farmer Was Replaced** (TFWR), a game where you program drones to automate farming tasks.

## Features

- **Unified Crop Interface:** Each crop module exposes a consistent `farm(area, amount)` function that auto-selects between parallel drones or single-threaded execution based on available unlocks.
- **Multi-Drone Parallelization:** Efficient drone spawning with looping functions (`run_func_until`, `run_func_looped`) to avoid spawn/despawn overhead.
- **Smart Resource Management:** `plot_management.py` farms resources until target amounts are reached.
- **Cost Calculation:** `cost_calculator.py` computes remaining items needed for unlocks (subtracts current inventory).
- **Maze Farming:** Dual-drone wall-following algorithms for gold farming.
- **Auto-Unlock:** Scripts to automatically progress through game unlocks (early to late game).

## Architecture

### Conventions

- **Area tuple:** `area = (pos, size)` where `pos = (x, y)` and `size = (width, height)`
- **Max 2 params:** Functions take at most 2 positional parameters. Extra config uses `options` dict.

### Crop Modules

Each crop module provides a consistent interface:

| Function | Description |
|----------|-------------|
| `plant_field(area)` | Plants/grows crops (no harvest) |
| `farm_field(area)` | Full cycle including harvest (pumpkins, cactus only) |
| `farm(area, amount)` | Farm until target amount reached (auto-selects parallel vs single-threaded) |

| Module | Item | Notes |
|--------|------|-------|
| `hay.py` | Hay | Simple plant and harvest |
| `carrots.py` | Carrot | Simple plant and harvest |
| `sunflowers.py` | Power | Simple plant and harvest |
| `trees.py` | Wood | Checkerboard pattern with bushes |
| `weird_substance.py` | Weird Substance | Checkerboard with fertilizer (requires Fertilizer unlock) |
| `pumpkins.py` | Pumpkin | Waits for growth, harvests merged group (yield = count^3) |
| `cactus.py` | Cactus | Plants, sorts ascending, chain-harvests (yield = count^2) |
| `gold.py` | Gold | Maze farming (requires Mazes unlock, ignores area param) |
| `dinosaurs.py` | Bone | Simple plant and harvest (requires Dinosaurs unlock) |

### Core Systems

| File | Purpose |
|------|---------|
| `main.py` | Entry point with test/target modes |
| `multi.py` | Drone parallelization (`run_func`, `run_func_until`, `run_func_looped`) |
| `plot_management.py` | High-level resource farming via `auto_plotter(area, amount_wanted)` |
| `movement.py` | Navigation with world-wrapping support |
| `crops.py` | Soil preparation, watering, and planting |
| `coordinates.py` | Area traversal patterns (NORMAL, SNAKE) |
| `utils.py` | Area mapping and slice generation |
| `cost_calculator.py` | Unlock cost calculation with inventory subtraction |
| `auto_unlock.py` | Full game progression automation (early to late game) |
| `hats.py` | Visual feedback via drone hats |

## Getting Started

1. Copy scripts into your TFWR save folder
2. Open the game and load your save
3. Run `main.py` to start automation

### Configuration

In `main.py`:
- Set `MODE = "test"` to farm a single crop continuously (set `TEST_CROP` to choose which)
- Set `MODE = "target"` to farm resources for a specific unlock

## Language Limitations

The scripting language is Python-like but **not actual Python**:
- No classes, lambdas, list comprehensions, or try/except
- Only `#` comments (no docstrings)
- No standard library - only game built-ins
- `__builtins__.py` contains type stubs for IDE support only

## Credits

Built-in type stubs contributed by @Noon, @KlingonDragon, @dieckie, and @Flekay on the TFWR Discord server.

---

*Community-created scripts, not officially affiliated with the game developers.*
