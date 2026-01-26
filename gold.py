import movement
import crops

direction_to_right = {North: East, East: South, South: West, West: North}
direction_to_left = {North: West, West: South, South: East, East: North}


def initialize_maze():
	movement.go_to((0, 0))
	crops.plant_crop(Entities.Bush)

	substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)


def traverse_maze_left():
	current_dir = North
	found_treasure = False

	while get_entity_type() == Entities.Hedge and found_treasure == False:
		right_dir = direction_to_right[current_dir]
		left_dir = direction_to_left[current_dir]
		back_dir = direction_to_right[right_dir]

		if can_move(left_dir):
			current_dir = left_dir
		elif can_move(current_dir):
			current_dir = current_dir
		elif can_move(right_dir):
			current_dir = right_dir
		else:
			current_dir = back_dir
		move(current_dir)

		if get_entity_type() == Entities.Treasure:
			found_treasure = True
			harvest()


def traverse_maze_right():
	current_dir = North
	found_treasure = False

	while get_entity_type() == Entities.Hedge and found_treasure == False:
		right_dir = direction_to_right[current_dir]
		left_dir = direction_to_left[current_dir]
		back_dir = direction_to_right[right_dir]

		if can_move(right_dir):
			current_dir = right_dir
		elif can_move(current_dir):
			current_dir = current_dir
		elif can_move(left_dir):
			current_dir = left_dir
		else:
			current_dir = back_dir
		move(current_dir)

		if get_entity_type() == Entities.Treasure:
			found_treasure = True
			harvest()


def farm_maze():
	initialize_maze()

	leftDrone = spawn_drone(traverse_maze_left)
	rightDrone = spawn_drone(traverse_maze_right)

	while has_finished(leftDrone) == False and has_finished(rightDrone) == False:
		do_a_flip()


# Farm gold until we have at least 'amount'
# Note: area param is ignored (mazes don't use area-based farming)
# Kept for consistent interface with other crop modules
def farm(area, amount):
	_ = area

	def has_enough():
		return num_items(Items.Gold) >= amount

	if has_enough():
		return

	while not has_enough():
		farm_maze()
