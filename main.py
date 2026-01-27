import multi
import utils
import movement
import plot_management
import cost_calculator

import hay
import trees
import carrots
import pumpkins
import sunflowers
import cactus
import weird_substance
import gold
import dinosaurs

clear()
# set_execution_speed(10)
set_world_size(32)

FULL_MAP = ((0, 0), (get_world_size(), get_world_size()))

# =============================================================================
# MODE: Set to "test" or "target"
# =============================================================================
MODE = "target"

# =============================================================================
# TEST MODE: Pick a crop to farm continuously
# Options: hay, trees, carrots, pumpkins, sunflowers, cactus, weird_substance, gold
# =============================================================================
TEST_CROP = "pumpkins"

test_funcs = {
	"hay": hay.plant_field,
	"trees": trees.plant_field,
	"carrots": carrots.plant_field,
	"pumpkins": pumpkins.farm_field,
	"sunflowers": sunflowers.plant_field,
	"cactus": cactus.farm_field,
	"weird_substance": weird_substance.plant_field,
	"gold": gold.farm_maze,
	"bone": dinosaurs.farm_field,
}

# =============================================================================
# TARGET MODE: Farm for a specific unlock
# =============================================================================
TARGET = Unlocks.Top_Hat


# =============================================================================
# Main
# =============================================================================
if MODE == "test":
	if TEST_CROP == "gold":
		while True:
			gold.farm_maze()
	elif TEST_CROP == "pumpkins":
		# Parallel plant, wait for all, then single harvest
		while True:
			multi.run_func(FULL_MAP, pumpkins.plant_field)
			movement.go_to((0, 0))
			harvest()
	elif TEST_CROP == "cactus":
		# Cactus handles its own parallelization internally
		while True:
			cactus.farm_field(FULL_MAP)
	elif TEST_CROP == "bone":
		dinosaurs.farm_field(FULL_MAP)
	else:
		multi.run_func_looped(FULL_MAP, test_funcs[TEST_CROP])

else:
	REQUESTED_ITEMS = cost_calculator.calculate_items_for_unlock_cost(TARGET)
	print(REQUESTED_ITEMS)

	def main():
		plot_management.auto_plotter(FULL_MAP, REQUESTED_ITEMS)

	utils.run_infinite(main)
