import movement
import utils
import crops

def plant_field(pos, size, secondary_entity):
	def plant_in_checkerboard(dest):
		movement.go_to(dest)
		if (dest[0] + dest[1]) % 2 == 0:
			crops.plant(Entities.Tree)
		else:
			crops.plant_crop(secondary_entity)
	utils.map_over_area(plant_in_checkerboard, pos, size)

	
	