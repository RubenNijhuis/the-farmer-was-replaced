import movement
import utils
import crops
import coordinates

def plant_field(pos, size):
	utils.map_over_area(
		crops.farm_crop_at(Entities.Sunflower),
		pos,
		size,
		"SNAKE"
	)

	

	
	