import utils
import crops
import multi


def plant_field(area):
	utils.map_over_area(area, crops.farm_crop_at(Entities.Grass), "SNAKE")


# Farm hay until we have at least 'amount'
# Uses parallel drones if Megafarm is unlocked, otherwise single-threaded
def farm(area, amount):
	def has_enough():
		return num_items(Items.Hay) >= amount

	if has_enough():
		return

	if num_unlocked(Unlocks.Megafarm) > 0:
		multi.run_func_until(area, plant_field, {"should_stop": has_enough})
	else:
		while not has_enough():
			plant_field(area)
