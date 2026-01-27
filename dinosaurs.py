# Dinosaur farming - Hamiltonian cycle (zigzag + row 0 return)

def get_direction():
	x, y = get_pos_x(), get_pos_y()
	size = get_world_size()

	if y == 0:
		if x > 0:
			return West
		return North
	if x == size - 1:
		return South
	if x % 2 == 0:
		if y < size - 1:
			return North
		return East
	if y > 1:
		return South
	return East


def farm_field(area):
	clear()
	set_world_size(32)
	change_hat(Hats.Dinosaur_Hat)

	while move(get_direction()):
		if get_entity_type() == Entities.Apple:
			pass

	change_hat(Hats.Straw_Hat)


def plant_field(area):
	farm_field(area)


def farm(area, amount):
	while num_items(Items.Bone) < amount:
		farm_field(area)
