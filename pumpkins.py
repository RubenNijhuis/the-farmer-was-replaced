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
				# if get_water() < 0.5:
				# 	use_item(Items.Water)
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
# Uses parallel planting (like main.py), then single harvest
def farm(area, amount):
	pos = area[0]

	while num_items(Items.Pumpkin) < amount:
		if num_unlocked(Unlocks.Megafarm) > 0:
			# Parallel plant, then single harvest
			multi.run_func(area, plant_field)
			movement.go_to(pos)
			harvest()
		else:
			# Single-threaded
			farm_field(area)
