import movement
import utils
import crops

DIRECTIONS = [North, East, South, West]

def initialize_maze():
	movement.go_to((0, 0))
	plant(Entities.Bush)

	substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)


def turn_right(direction):
	return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]


def turn_left(direction):
	return DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]


def turn_back(direction):
	return DIRECTIONS[(DIRECTIONS.index(direction) + 2) % 4]


def farm_maze():
	initialize_maze()
	current_dir = North

	while True:
		right = turn_right(current_dir)
		left = turn_left(current_dir)
		back = turn_back(current_dir)

		if can_move(right):
			current_dir = right
		elif can_move(current_dir):
			current_dir = current_dir
		elif can_move(left):
			current_dir = left
		else:
			current_dir = back

		move(current_dir)

		if get_entity_type() == Entities.Treasure:
			break

	harvest()