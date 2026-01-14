import utils
import crops
import trees
import pumpkins
import cactus
import gold
import hats
import sunflowers
import movement

START_MAP = (0,0)
FULL_SIZE = (get_world_size(), get_world_size())

def plot_for_power():
	sunflowers.plant_field(
		START_MAP,
		FULL_SIZE
	)

def plot_for_hay():
	utils.map_over_area(
		crops.farm_crop_at(Entities.Grass),
		START_MAP,
		FULL_SIZE
	)

def plot_for_wood():
	trees.plant_field(
		START_MAP,
		FULL_SIZE,
		Entities.Bush
	)

def plot_for_carrot():
	utils.map_over_area(
		crops.farm_crop_at(Entities.Carrot),
		START_MAP,
		FULL_SIZE
	)

def plot_for_pumpkin():
	amount_slices = get_world_size() // max_drones()
	slice_width = get_world_size() / amount_slices	
	
	drones = []
	all_finished = False
	
	for i in range(amount_slices):
		pos_x = 0
		pos_y = slice_width * i
		w = get_world_size()
		h = slice_width
		
		def plant_func():
			pumpkins.plant_field((pos_x, pos_y), (w, h))
		
		def zero_wrapper():
			return plant_func()
		
		movement.go_to((pos_x, pos_y))
		drone = spawn_drone(plant_func)
		
	while all_finished == False:
		all_finished = True
		for i in drones:
			if has_finished(drones[i]) == False:
				all_finished = False
	
	movement.go_to(START_MAP)
	harvest()

def plot_for_cactus():
	cactus.plant_field(START_MAP, FULL_SIZE)

def plot_for_weird_substance():
	def plant_tree_with_weird_substance(pos):
		movement.go_to(pos)
		if num_items(Items.Fertilizer) > 1000:
			use_item(Items.Fertilizer)
			if pos[0] % 2 == 0 and pos[1] % 2 == 0:
				crops.plant_crop(Entities.Tree)
			elif pos[0] % 2 == 1 and pos[1] % 2 == 1:
				crops.plant_crop(Entities.Tree)
			else:
				crops.plant_crop(Entities.Grass)

	utils.map_over_map(plot_for_weird_substance)

def plot_for_gold():
	gold.farm_maze()

plot_function_for_item = {
	Items.Power:           plot_for_power,
	Items.Hay:             plot_for_hay,
	Items.Wood:            plot_for_wood,
	Items.Carrot:          plot_for_carrot,
	Items.Pumpkin:         plot_for_pumpkin,
	Items.Cactus:          plot_for_cactus,
	Items.Weird_Substance: plot_for_weird_substance,
	Items.Gold:            plot_for_gold
}

def auto_plotter(minimum_amounts):
	for item in minimum_amounts:
		if num_items(item) < minimum_amounts[item]:
			change_hat(hats.hat_for_item[item])
			plot_function_for_item[item]()