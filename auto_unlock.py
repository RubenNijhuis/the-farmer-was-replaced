import cost_calculator
import crops
import movement
import coordinates

import hay
import trees
import carrots
import sunflowers
import pumpkins
import cactus
import weird_substance
import gold
import dinosaurs

# Maps items to their farm functions (requires Plant unlock)
farm_func_for_item = {
	Items.Hay: hay.farm,
	Items.Wood: trees.farm,
	Items.Carrot: carrots.farm,
	Items.Power: sunflowers.farm,
	Items.Pumpkin: pumpkins.farm,
	Items.Cactus: cactus.farm,
	Items.Weird_Substance: weird_substance.farm,
	Items.Gold: gold.farm,
	Items.Bone: dinosaurs.farm,
}

# Order of unlocks for game progression
unlock_order = [
	# Early game - basic resources
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Plant,
	Unlocks.Expand,
	Unlocks.Speed,
	Unlocks.Carrots,
	Unlocks.Expand,
	Unlocks.Speed,
	Unlocks.Watering,
	Unlocks.Trees,
	Unlocks.Grass,
	Unlocks.Trees,
	Unlocks.Trees,
	Unlocks.Carrots,
	Unlocks.Sunflowers,
	Unlocks.Expand,
	Unlocks.Pumpkins,
	# Mid game - advanced crops
	Unlocks.Speed,
	Unlocks.Pumpkins,
	Unlocks.Expand,
	Unlocks.Cactus,
	Unlocks.Speed,
	Unlocks.Cactus,
	Unlocks.Expand,
	Unlocks.Fertilizer,
	Unlocks.Cactus,
	Unlocks.Mazes,
	Unlocks.Expand,
	Unlocks.Mazes,
	Unlocks.Speed,
	Unlocks.Dinosaurs,
	# Late game - optimization
	Unlocks.Expand,
	Unlocks.Dinosaurs,
	Unlocks.Polyculture,
	Unlocks.Megafarm,
	Unlocks.Leaderboard,
]


def get_area():
	# Returns current world as area tuple
	size = get_world_size()
	return ((0, 0), (size, size))


# Early game: harvest grass without planting (before Plant is unlocked)
def harvest_hay_early(amount):
	while num_items(Items.Hay) < amount:
		coords = coordinates.generate_coords(get_area(), "NORMAL")
		for pos in coords:
			if num_items(Items.Hay) >= amount:
				return
			movement.go_to(pos)
			if can_harvest():
				harvest()


# Early game: farm wood using bushes (before Trees is unlocked)
def farm_wood_early(amount):
	while num_items(Items.Wood) < amount:
		coords = coordinates.generate_coords(get_area(), "NORMAL")
		for pos in coords:
			if num_items(Items.Wood) >= amount:
				return
			movement.go_to(pos)
			if get_entity_type() == Entities.Bush:
				if can_harvest():
					harvest()
			plant(Entities.Bush)


# Early game: farm carrots (before full module features available)
def farm_carrots_early(amount):
	while num_items(Items.Carrot) < amount:
		coords = coordinates.generate_coords(get_area(), "NORMAL")
		for pos in coords:
			if num_items(Items.Carrot) >= amount:
				return
			movement.go_to(pos)
			if get_entity_type() == Entities.Carrot:
				if can_harvest():
					harvest()
			if num_unlocked(Unlocks.Watering) > 0:
				if get_water() < 0.5:
					use_item(Items.Water)
			plant(Entities.Carrot)


def farm_item(item, amount):
	# Early game: before Plant is unlocked, only harvest naturally
	if num_unlocked(Unlocks.Plant) == 0:
		if item == Items.Hay:
			harvest_hay_early(amount)
		return

	# Early game: use bushes for wood before Trees is unlocked
	if item == Items.Wood and num_unlocked(Entities.Tree) == 0:
		farm_wood_early(amount)
		return

	# Early game: simple carrot farming before Watering/Grass unlocks
	if item == Items.Carrot and num_unlocked(Unlocks.Grass) == 0:
		farm_carrots_early(amount)
		return

	# Weird substance requires Fertilizer to be unlocked
	if item == Items.Weird_Substance and num_unlocked(Unlocks.Fertilizer) == 0:
		quick_print("Weird Substance needs Fertilizer unlock")
		return

	# Gold requires Mazes to be unlocked
	if item == Items.Gold and num_unlocked(Unlocks.Mazes) == 0:
		quick_print("Gold needs Mazes unlock")
		return

	# Check if the crop for this item is unlocked
	if item in crops.entity_for_item:
		entity = crops.entity_for_item[item]
		if num_unlocked(entity) == 0:
			quick_print(item, " crop not unlocked yet")
			return

	# Get the farm function and call it
	if item in farm_func_for_item:
		farm_func = farm_func_for_item[item]
		farm_func(get_area(), amount)
	else:
		quick_print("No farm function for ", item)


def main():
	for unlock_item in unlock_order:
		# Get remaining items needed (subtracts current inventory)
		items = cost_calculator.calculate_remaining_cost(unlock_item)

		quick_print("Unlocking ", unlock_item, " Cost ", items)

		# Farm each required item
		for i in range(len(items)):
			item, amount = items[i]
			farm_item(item, amount)

		unlock(unlock_item)
		quick_print("Unlocked ", unlock_item, " at ", get_time())

	quick_print("All unlocks complete!")
	while True:
		do_a_flip()


main()
