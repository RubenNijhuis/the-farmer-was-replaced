import movement
import crops
import weird_substance

direction_to_right = {North: East, East: South, South: West, West: North}
direction_to_left = {North: West, West: South, South: East, East: North}


def get_substance_per_maze():
	return get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)


def get_gold_per_maze():
	# Treasure gives gold equal to the maze side length
	# Maze side length = weird substance used
	return get_substance_per_maze()


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

	# If Megafarm not unlocked, use single drone traversal
	if num_unlocked(Unlocks.Megafarm) == 0:
		traverse_maze_left()
		return

	# With Megafarm, race two drones (left and right wall-following)
	# Spawn one drone for left traversal, main drone does right traversal
	leftDrone = spawn_drone(traverse_maze_left)
	traverse_maze_right()  # Main drone traverses too

	# Wait for the other drone if it hasn't finished
	if not has_finished(leftDrone):
		wait_for(leftDrone)


# Farm gold until we have at least 'amount'
# Note: area param is used for farming weird substance
def farm(area, amount):
	def has_enough_gold():
		return num_items(Items.Gold) >= amount

	if has_enough_gold():
		return

	substance_per_maze = get_substance_per_maze()
	gold_per_maze = get_gold_per_maze()

	while not has_enough_gold():
		# Calculate how many mazes we need to reach goal
		gold_needed = amount - num_items(Items.Gold)
		mazes_needed = (gold_needed // gold_per_maze) + 1

		# Farm weird substance in batches (enough for 10 mazes or remaining, whichever is smaller)
		batch_size = min(mazes_needed, 10)
		substance_needed = batch_size * substance_per_maze
		current_substance = num_items(Items.Weird_Substance)

		if current_substance < substance_needed:
			quick_print("[gold] Farming weird substance: need ", substance_needed, " have ", current_substance)
			weird_substance.farm(area, substance_needed)

		# Run mazes until we run out of substance or have enough gold
		while num_items(Items.Weird_Substance) >= substance_per_maze and not has_enough_gold():
			farm_maze()
