import utils
import crops
import pumpkins
import cactus
import gold

START_MAP = (0,0)
FULL_SIZE = (get_world_size(), get_world_size())

def plot_for_power():
	max_farmers = max_drones()
	
	slices = max(1, get_world_size() // max_farmers)
	slice_width = 10		
	finished_drones = 0
	drones = []
	for i in range(slices):
		pos_x, pos_y = slice_width * i, 0 
		def farm_sun():
			utils.map_over_area(
				crops.farm_crop_at(Entities.Sunflower),
				(pos_x, pos_y),
				(slice_width, get_world_size())
			)
		
		drone = spawn_drone(farm_sun)
		drones.append(drone)
		wait_for(drone)
	
	while True:
		finished_drones = 0
		if drone in drones:
			if has_finished(drone):
				finished_drones += 1
		
		if finished_drones == len(drones):
			return

def plot_for_hay():
	utils.map_over_map(crops.farm_crop_at(Entities.Sunflower))

def plot_for_wood():
	def plant_trees(pos):
		movement.go_to(pos)
		if pos[0] % 2 == 0 and pos[1] % 2 == 0:
			crops.plant_crop(Entities.Tree)
		elif pos[0] % 2 == 1 and pos[1] % 2 == 1:
			crops.plant_crop(Entities.Tree)
		else:
			crops.plant_crop(Entities.Bush)

def plot_for_carrot():
	utils.map_over_map(crops.farm_crop_at(Entities.Carrot))

def plot_for_pumpkin():
	pumpkins.farm_pumpkin_field(START_MAP, FULL_SIZE)

def plot_for_cactus():
	cactus.farm_cactus_field(START_MAP, FULL_SIZE)

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

hat_for_item = {
	Items.Power:           Hats.Sunflower_Hat,
	Items.Hay:             Hats.Straw_Hat,
	Items.Wood:            Hats.Tree_Hat,
	Items.Carrot:          Hats.Carrot_Hat,
	Items.Pumpkin:         Hats.Pumpkin_Hat,
	Items.Cactus:          Hats.Green_Hat,
	Items.Weird_Substance: Hats.Wizard_Hat,
	Items.Gold:            Hats.Gold_Hat
}

def auto_plotter(minimum_amounts):
	for item in minimum_amounts:
		if num_items(item) < minimum_amounts[item]:
			change_hat(hat_for_item[item])
			plot_function_for_item[item]()