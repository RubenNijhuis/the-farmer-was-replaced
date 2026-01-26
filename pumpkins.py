import movement
import coordinates
import crops
import multi


# Plants pumpkins and waits for all to grow (no harvest)
def plant_field(area):
	replant_record = coordinates.generate_coords(area, "SNAKE")

	while replant_record:
		next_round = []

		for position in replant_record:
			movement.go_to(position)
			entity = get_entity_type()

			if entity != Entities.Pumpkin:
				if get_water() < 0.5:
					use_item(Items.Water)
				crops.plant_crop(Entities.Pumpkin)
				next_round.append(position)
			elif not can_harvest():
				next_round.append(position)

		replant_record = next_round


# Full cycle: plant, wait for growth, then harvest merged pumpkins
def farm_field(area):
	pos = area[0]
	plant_field(area)
	movement.go_to(pos)
	harvest()


# Farm pumpkins until we have at least 'amount'
# Uses parallel drones if Megafarm is unlocked, otherwise single-threaded
# Note: Uses farm_field (not plant_field) because pumpkins need final harvest
def farm(area, amount):
	def has_enough():
		return num_items(Items.Pumpkin) >= amount

	if has_enough():
		return

	if num_unlocked(Unlocks.Megafarm) > 0:
		multi.run_func_until(area, farm_field, {"should_stop": has_enough})
	else:
		while not has_enough():
			farm_field(area)
