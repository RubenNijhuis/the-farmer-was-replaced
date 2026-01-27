import movement

grounds_for_entity = {
	Entities.Grass: Grounds.Grassland,
	Entities.Bush: Grounds.Grassland,
	Entities.Tree: Grounds.Grassland,
	Entities.Carrot: Grounds.Soil,
	Entities.Pumpkin: Grounds.Soil,
	Entities.Dead_Pumpkin: Grounds.Soil,
	Entities.Sunflower: Grounds.Soil,
	Entities.Cactus: Grounds.Soil,
	Entities.Dinosaur: Grounds.Soil,
}

entity_for_item = {
	Items.Power: Entities.Sunflower,
	Items.Hay: Entities.Grass,
	Items.Wood: Entities.Bush,
	Items.Carrot: Entities.Carrot,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Cactus: Entities.Cactus,
	Items.Bone: Entities.Dinosaur,
}

item_for_entity = {
	Entities.Sunflower: Items.Power,
	Entities.Grass: Items.Hay,
	Entities.Bush: Items.Wood,
	Entities.Carrot: Items.Carrot,
	Entities.Pumpkin: Items.Pumpkin,
	Entities.Cactus: Items.Cactus,
	Entities.Dinosaur: Items.Bone,
}

amount_from_harvest = {
	Entities.Grass: 512,
	Entities.Bush: 512,
	Entities.Tree: 512,
	Entities.Carrot: 512,
	Entities.Pumpkin: 3145728,
	Entities.Sunflower: 10,
	Entities.Cactus: 10,
}


def try_harvest():
	if can_harvest():
		harvest()


def set_soil_for_crop(crop):
	if get_ground_type() != grounds_for_entity[crop]:
		till()


def plant_crop(crop):
	try_harvest()
	set_soil_for_crop(crop)
	# use_item(Items.Water)
	plant(crop)


def farm_crop_at(entity):
	def at(pos):
		movement.go_to(pos)
		plant_crop(entity)

	return at
