import crops
import movement

def drone_plant_at(plant, pos):
	def task():
		movement.go_to(pos)
		crops.plant_crop(plant)
		crops.try_harvest()
	return task

def plant_field(area):
	pos, size = area
	plant_list = [Entities.Carrot, Entities.Carrot, Entities.Carrot]

	sx, sy = pos[0] + (size[0] / 2) - 1, pos[1] + (size[1] / 2) - 1
	movement.go_to((sx, sy))
	while True:
		for item in plant_list:
			crops.plant_crop(item)
			plant_type, (x, y) = get_companion()
			plant_drone = spawn_drone(drone_plant_at(plant_type, (x, y)))
			wait_for(plant_drone)
