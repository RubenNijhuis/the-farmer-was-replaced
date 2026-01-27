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
# Upgradable unlocks: Trees, Carrots, Grass, Pumpkins, Cactus, Mazes, Dinosaurs, Speed, Expand, Sunflowers
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
	Unlocks.Carrots,  # Extra carrot upgrade for better yield
	Unlocks.Sunflowers,
	Unlocks.Grass,  # Extra grass upgrade
	Unlocks.Expand,
	Unlocks.Pumpkins,
	# Mid game - advanced crops
	Unlocks.Speed,
	Unlocks.Pumpkins,
	Unlocks.Pumpkins,  # Extra pumpkin upgrade (yield = count^3)
	Unlocks.Expand,
	Unlocks.Cactus,
	Unlocks.Speed,
	Unlocks.Cactus,
	Unlocks.Cactus,  # Extra cactus upgrade (yield = count^2)
	Unlocks.Expand,
	Unlocks.Fertilizer,
	Unlocks.Cactus,  # More cactus upgrades
	Unlocks.Mazes,
	Unlocks.Expand,
	Unlocks.Mazes,
	Unlocks.Mazes,  # Extra maze upgrade for more gold
	Unlocks.Speed,
	Unlocks.Dinosaurs,
	# Late game - optimization
	Unlocks.Expand,
	Unlocks.Dinosaurs,
	Unlocks.Dinosaurs,  # Extra dinosaur upgrade
	Unlocks.Speed,
	Unlocks.Speed,  # Max speed helps a lot
	Unlocks.Polyculture,
	Unlocks.Megafarm,
	# Post-megafarm upgrades (parallel farming makes these faster)
	Unlocks.Trees,  # More tree upgrades now that we have megafarm
	Unlocks.Trees,
	Unlocks.Carrots,
	Unlocks.Pumpkins,
	Unlocks.Cactus,
	Unlocks.Mazes,
	Unlocks.Dinosaurs,
	Unlocks.Expand,  # Max expand
	Unlocks.Leaderboard,
]


def get_area():
	# Returns current world as area tuple
	size = get_world_size()
	return ((0, 0), (size, size))


# Early game: harvest grass without planting (before Plant is unlocked)
def harvest_hay_early(amount):
	quick_print("[early] Harvesting hay: ", num_items(Items.Hay), "/", amount)
	while num_items(Items.Hay) < amount:
		coords = coordinates.generate_coords(get_area(), "NORMAL")
		for pos in coords:
			if num_items(Items.Hay) >= amount:
				quick_print("[early] Done hay: ", num_items(Items.Hay))
				return
			movement.go_to(pos)
			if can_harvest():
				harvest()
		quick_print("[early] Hay progress: ", num_items(Items.Hay), "/", amount)
	quick_print("[early] Done hay: ", num_items(Items.Hay))


# Early game: farm wood using bushes (before Trees is unlocked)
def farm_wood_early(amount):
	quick_print("[early] Farming wood (bushes): ", num_items(Items.Wood), "/", amount)
	pass_count = 0
	while num_items(Items.Wood) < amount:
		coords = coordinates.generate_coords(get_area(), "NORMAL")
		for pos in coords:
			if num_items(Items.Wood) >= amount:
				quick_print("[early] Done wood: ", num_items(Items.Wood))
				return
			movement.go_to(pos)
			if get_entity_type() == Entities.Bush:
				if can_harvest():
					harvest()
			# Bushes need grassland - till soil back to grassland
			if get_ground_type() != Grounds.Grassland:
				till()
			plant(Entities.Bush)
		pass_count = pass_count + 1
		if pass_count % 3 == 0:
			quick_print("[early] Wood progress: ", num_items(Items.Wood), "/", amount)
	quick_print("[early] Done wood: ", num_items(Items.Wood))


# Early game: farm carrots (before full module features available)
def farm_carrots_early(amount):
	quick_print("[early] Farming carrots: ", num_items(Items.Carrot), "/", amount)
	pass_count = 0
	while num_items(Items.Carrot) < amount:
		coords = coordinates.generate_coords(get_area(), "NORMAL")
		for pos in coords:
			if num_items(Items.Carrot) >= amount:
				quick_print("[early] Done carrots: ", num_items(Items.Carrot))
				return
			movement.go_to(pos)
			if get_entity_type() == Entities.Carrot:
				if can_harvest():
					harvest()
			# Carrots need soil - till grassland to soil
			if get_ground_type() != Grounds.Soil:
				till()
			if num_unlocked(Unlocks.Watering) > 0:
				if get_water() < 0.5:
					use_item(Items.Water)
			plant(Entities.Carrot)
		pass_count = pass_count + 1
		if pass_count % 3 == 0:
			quick_print("[early] Carrot progress: ", num_items(Items.Carrot), "/", amount)
	quick_print("[early] Done carrots: ", num_items(Items.Carrot))


def farm_item(item, amount):
	current = num_items(item)
	quick_print("  Farming ", item, ": ", current, "/", amount)

	# Early game: before Plant is unlocked, only harvest naturally
	if num_unlocked(Unlocks.Plant) == 0:
		if item == Items.Hay:
			harvest_hay_early(amount)
		else:
			quick_print("  SKIP: Plant not unlocked, can only harvest hay")
		return

	# Early game: use bushes for wood before Trees is unlocked
	if item == Items.Wood and num_unlocked(Entities.Tree) == 0:
		quick_print("  Using early wood farming (bushes)")
		farm_wood_early(amount)
		return

	# Early game: simple carrot farming before Watering/Grass unlocks
	if item == Items.Carrot and num_unlocked(Unlocks.Grass) == 0:
		quick_print("  Using early carrot farming")
		farm_carrots_early(amount)
		return

	# Weird substance requires Fertilizer to be unlocked
	if item == Items.Weird_Substance and num_unlocked(Unlocks.Fertilizer) == 0:
		quick_print("  BLOCKED: Weird Substance needs Fertilizer unlock")
		return

	# Gold requires Mazes to be unlocked
	if item == Items.Gold and num_unlocked(Unlocks.Mazes) == 0:
		quick_print("  BLOCKED: Gold needs Mazes unlock")
		return

	# Check if the crop for this item is unlocked
	if item in crops.entity_for_item:
		entity = crops.entity_for_item[item]
		if num_unlocked(entity) == 0:
			quick_print("  BLOCKED: ", item, " crop not unlocked yet")
			return

	# Get the farm function and call it
	if item in farm_func_for_item:
		farm_func = farm_func_for_item[item]
		quick_print("  Starting farm for ", item, " (need ", amount - current, " more)")
		farm_func(get_area(), amount)
		quick_print("  Done farming ", item, ": ", num_items(item))
	else:
		quick_print("  ERROR: No farm function for ", item)


def main():
	total_unlocks = len(unlock_order)
	quick_print("=== AUTO UNLOCK START ===")
	quick_print("Total unlocks to process: ", total_unlocks)

	for idx in range(total_unlocks):
		unlock_item = unlock_order[idx]
		current_level = num_unlocked(unlock_item)

		quick_print("")
		quick_print("=== [", idx + 1, "/", total_unlocks, "] ", unlock_item, " ===")
		quick_print("Current level: ", current_level)
		quick_print("World size: ", get_world_size(), "x", get_world_size())

		# Check if unlock is available (get_cost returns None if not available/already maxed)
		cost = get_cost(unlock_item)
		if cost == None:
			quick_print("SKIP: Unlock not available or already maxed")
			continue

		# Get TOTAL items needed for this unlock (not remaining)
		items = cost_calculator.calculate_items_for_unlock_cost(unlock_item)

		if len(items) == 0:
			quick_print("Already have enough resources!")
		else:
			quick_print("Resources needed (total):")
			for i in range(len(items)):
				item, amount = items[i]
				have = num_items(item)
				if have >= amount:
					quick_print("  - ", item, ": ", amount, " (have ", have, ") OK")
				else:
					quick_print("  - ", item, ": ", amount, " (have ", have, ") need ", amount - have, " more")

		# Farm each required item to reach TOTAL target
		for i in range(len(items)):
			item, amount = items[i]
			if num_items(item) >= amount:
				quick_print("  Already have enough ", item)
				continue
			farm_item(item, amount)

		# Debug: show final inventory before unlock attempt
		quick_print("Inventory before unlock:")
		quick_print("  Hay:", num_items(Items.Hay), " Wood:", num_items(Items.Wood), " Carrot:", num_items(Items.Carrot))

		# Attempt unlock
		quick_print("Attempting unlock...")
		result = unlock(unlock_item)
		if result:
			quick_print("SUCCESS: ", unlock_item, " now level ", num_unlocked(unlock_item))
		else:
			# Debug why it failed
			quick_print("FAILED to unlock ", unlock_item, "!")
			actual_cost = get_cost(unlock_item)
			if actual_cost == None:
				quick_print("  Reason: Unlock not available (prerequisite missing?)")
			else:
				quick_print("  Required cost: ", actual_cost)
				for cost_item in actual_cost:
					have = num_items(cost_item)
					need = actual_cost[cost_item]
					if have < need:
						quick_print("  MISSING: ", cost_item, " have ", have, " need ", need)
		quick_print("Time: ", get_time())

	quick_print("")
	quick_print("=== ALL UNLOCKS COMPLETE ===")
	quick_print("Total time: ", get_time())
	while True:
		do_a_flip()


main()