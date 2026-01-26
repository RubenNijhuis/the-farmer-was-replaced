import utils
import crops
import multi


def get_biggest_in_list(coords):
	biggest_pos = (0, 0)
	biggest_petals = 0

	for pos in coords:
		if get_entity_type() != Entities.Sunflower:
			continue
		petals = measure()
		if petals > biggest_petals:
			biggest_petals = petals
			biggest_pos = pos
	return biggest_pos


def plant_field(area):
	utils.map_over_area(area, crops.farm_crop_at(Entities.Sunflower), "SNAKE")


# Farm power until we have at least 'amount'
# Uses parallel drones if Megafarm is unlocked, otherwise single-threaded
def farm(area, amount):
	def has_enough():
		return num_items(Items.Power) >= amount

	if has_enough():
		return

	if num_unlocked(Unlocks.Megafarm) > 0:
		multi.run_func_until(area, plant_field, {"should_stop": has_enough})
	else:
		while not has_enough():
			plant_field(area)
