import movement
import utils
import crops

def initialize_maze():
	movement.go_to((0,0))
	
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)

direction_to_right = {North:East, East:South, South:West, West:North}
direction_to_left = {North:West, West:South, South:East, East:North}

def farm_maze():
	initialize_maze()
	
	reached_gold = False
	current_dir = North
		
	while reached_gold == False:
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
			reached_gold = True
			
	harvest()
	
	
	
	
	
	