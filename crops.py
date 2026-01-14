import movement

grounds_for_entity = {
	Entities.Grass:			Grounds.Grassland,
	Entities.Bush:			Grounds.Grassland,
	Entities.Tree:			Grounds.Grassland,
	Entities.Carrot:		Grounds.Soil,
	Entities.Pumpkin:		Grounds.Soil,
	Entities.Dead_Pumpkin:	Grounds.Soil,
	Entities.Sunflower:		Grounds.Soil,
	Entities.Cactus:		Grounds.Soil
}

entity_for_item = {
	Items.Power: 			Entities.Sunflower,
	Items.Hay:				Entities.Grass,
	Items.Wood: 			Entities.Bush,
	Items.Carrot: 			Entities.Carrot,
	Items.Pumpkin: 			Entities.Pumpkin,
	Items.Cactus: 			Entities.Cactus,
}

def try_harvest():
	if can_harvest():
		harvest()

def set_soil_for_crop(crop):
	if (get_ground_type() != grounds_for_entity[crop]):
		till()

def plant_crop(crop):
	try_harvest()
	set_soil_for_crop(crop)
	plant(crop)

def farm_crop_at(crop):
	def wrapper(pos):
		movement.go_to(pos)
		plant_crop(crop)
	return wrapper