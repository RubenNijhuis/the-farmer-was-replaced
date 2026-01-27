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

unlock_order = [
	# === PHASE 1: Bootstrap (alternating) ===
	Unlocks.Speed,        # 1
	Unlocks.Expand,       # 1
	Unlocks.Plant,
	Unlocks.Speed,        # 2
	Unlocks.Expand,       # 2
	Unlocks.Carrots,      # 1
	Unlocks.Speed,        # 3
	Unlocks.Expand,       # 3
	Unlocks.Watering,     # 1
	Unlocks.Trees,        # 1
	Unlocks.Speed,        # 4
	Unlocks.Expand,       # 4
	Unlocks.Grass,        # 1
	Unlocks.Speed,        # 5 (MAX)
	Unlocks.Pumpkins,     # 1 - MUST be before Expand 5!
	Unlocks.Expand,       # 5
	Unlocks.Grass,        # 2

	# === PHASE 2: Rush to Megafarm (alternating) ===
	Unlocks.Trees,        # 2
	Unlocks.Carrots,      # 2
	Unlocks.Pumpkins,     # 2
	Unlocks.Trees,        # 3
	Unlocks.Carrots,      # 3
	Unlocks.Pumpkins,     # 3
	Unlocks.Watering,     # 2
	Unlocks.Trees,        # 4
	Unlocks.Carrots,      # 4
	Unlocks.Pumpkins,     # 4
	Unlocks.Grass,        # 3
	Unlocks.Expand,       # 6
	Unlocks.Sunflowers,
	Unlocks.Trees,        # 5
	Unlocks.Carrots,      # 5
	Unlocks.Pumpkins,     # 5
	Unlocks.Grass,        # 4
	Unlocks.Expand,       # 7
	Unlocks.Trees,        # 6
	Unlocks.Carrots,      # 6
	Unlocks.Watering,     # 3
	Unlocks.Fertilizer,   # 1
	Unlocks.Grass,        # 6
	Unlocks.Watering,     # 4
	Unlocks.Fertilizer,   # 2
	Unlocks.Mazes,        # 1

	# === PHASE 3: Megafarm + Grass to 8 + Pumpkins to 7 + Expand MAX (alternating) ===
	Unlocks.Megafarm,     # 1
	Unlocks.Grass,        # 7
	Unlocks.Pumpkins,     # 6
	Unlocks.Trees,        # 7
	Unlocks.Megafarm,     # 2
	Unlocks.Carrots,      # 7
	Unlocks.Expand,       # 8
	Unlocks.Trees,        # 8
	Unlocks.Cactus,       # 1
	Unlocks.Megafarm,     # 3
	Unlocks.Carrots,      # 8
	Unlocks.Megafarm,     # 4
	Unlocks.Grass,        # 8
	Unlocks.Expand,       # 9 (MAX)
	Unlocks.Megafarm,     # 5 (MAX)

	# === PHASE 4: Parallel farm yields + Cactus (alternating) ===
	Unlocks.Cactus,       # 2
	Unlocks.Cactus,       # 3
	Unlocks.Mazes,        # 2

	# === PHASE 5: Dinosaurs + remaining (alternating) ===
	Unlocks.Dinosaurs,    # 1
	Unlocks.Dinosaurs,    # 2
	Unlocks.Fertilizer,   # 3
	Unlocks.Dinosaurs,    # 3
	Unlocks.Dinosaurs,    # 4
	Unlocks.Dinosaurs,    # 5
	Unlocks.Dinosaurs,    # 6 (MAX)
	Unlocks.Leaderboard,
]


def get_area():
	size = get_world_size()
	return ((0, 0), (size, size))


def harvest_hay_early(amount):
	while num_items(Items.Hay) < amount:
		coords = coordinates.generate_coords(get_area(), "NORMAL")
		for pos in coords:
			if num_items(Items.Hay) >= amount:
				return
			movement.go_to(pos)
			if can_harvest():
				harvest()


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
			if get_ground_type() != Grounds.Grassland:
				till()
			plant(Entities.Bush)


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
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Carrot)


def farm_item(item, amount):
	if num_unlocked(Unlocks.Plant) == 0:
		if item == Items.Hay:
			harvest_hay_early(amount)
		return

	if item == Items.Wood and num_unlocked(Entities.Tree) == 0:
		farm_wood_early(amount)
		return

	if item == Items.Carrot and num_unlocked(Unlocks.Grass) == 0:
		farm_carrots_early(amount)
		return

	if item == Items.Weird_Substance and num_unlocked(Unlocks.Fertilizer) == 0:
		return

	if item == Items.Gold and num_unlocked(Unlocks.Mazes) == 0:
		return

	if item in crops.entity_for_item:
		entity = crops.entity_for_item[item]
		if num_unlocked(entity) == 0:
			return

	if item in farm_func_for_item:
		farm_func = farm_func_for_item[item]
		farm_func(get_area(), amount)


def main():
	total = len(unlock_order)

	for idx in range(total):
		unlock_item = unlock_order[idx]

		quick_print("[", idx + 1, "/", total, "] ", unlock_item)

		cost = get_cost(unlock_item)
		if cost == None:
			continue

		items = cost_calculator.calculate_items_for_unlock_cost(unlock_item)

		for i in range(len(items)):
			item, amount = items[i]
			if num_items(item) >= amount:
				continue
			farm_item(item, amount)

		result = unlock(unlock_item)
		if not result:
			quick_print("FAILED: ", unlock_item)
			actual_cost = get_cost(unlock_item)
			if actual_cost != None:
				for cost_item in actual_cost:
					have = num_items(cost_item)
					need = actual_cost[cost_item]
					if have < need:
						quick_print("  Missing ", cost_item, ": ", have, "/", need)
			while True:
				do_a_flip()

	quick_print("=== COMPLETE === Time: ", get_time())


main()
