# Dinosaur farming - snake game mechanics
# Equip hat, collect apples to grow tail, harvest bones = tail_length²

def get_blocked_positions(path_history, tail_length):
	# Returns set of positions blocked by tail
	# Last tail segment moves out of the way, so exclude it
	if tail_length <= 1:
		return set()

	start_idx = len(path_history) - tail_length
	if start_idx < 0:
		start_idx = 0

	# Exclude the last position (tail tip moves out of way)
	end_idx = len(path_history) - 1

	blocked = set()
	for i in range(start_idx, end_idx):
		blocked.add(path_history[i])

	return blocked


def bfs_find_path(start, target, blocked):
	# BFS pathfinding avoiding blocked positions
	# Returns list of directions, or None if no path
	size = get_world_size()

	if start == target:
		return []

	# Use parent dict instead of storing paths (much faster)
	# came_from[pos] = (parent_pos, direction_taken)
	came_from = {start: None}

	# Use index instead of slicing queue (avoids creating new lists)
	queue = [start]
	idx = 0

	while idx < len(queue):
		cx, cy = queue[idx]
		idx = idx + 1

		# Try all directions (prioritize toward target)
		tx, ty = target
		neighbors = []
		if ty > cy:
			neighbors.append(((cx, cy + 1), North))
		if ty < cy:
			neighbors.append(((cx, cy - 1), South))
		if tx > cx:
			neighbors.append(((cx + 1, cy), East))
		if tx < cx:
			neighbors.append(((cx - 1, cy), West))
		# Add remaining directions
		if ty <= cy:
			neighbors.append(((cx, cy + 1), North))
		if ty >= cy:
			neighbors.append(((cx, cy - 1), South))
		if tx <= cx:
			neighbors.append(((cx + 1, cy), East))
		if tx >= cx:
			neighbors.append(((cx - 1, cy), West))

		for next_pos, direction in neighbors:
			nx, ny = next_pos

			# Check bounds (no wrapping for dinosaur)
			if nx < 0 or nx >= size or ny < 0 or ny >= size:
				continue

			# Skip if already visited
			if next_pos in came_from:
				continue

			# Check if blocked by tail
			if next_pos in blocked:
				continue

			came_from[next_pos] = ((cx, cy), direction)

			if next_pos == target:
				# Reconstruct path by walking backwards
				path = []
				pos = target
				while came_from[pos] != None:
					parent, direction = came_from[pos]
					path.append(direction)
					pos = parent
				# Reverse the path
				reversed_path = []
				for i in range(len(path) - 1, -1, -1):
					reversed_path.append(path[i])
				return reversed_path

			queue.append(next_pos)

	return None


def farm_field(area):
	# Run the snake game on the whole field
	# Area parameter ignored - dinosaur uses entire farm
	clear()
	change_hat(Hats.Dinosaur_Hat)

	# Track movement history for tail collision
	path_history = [(get_pos_x(), get_pos_y())]
	tail_length = 0

	# Apple spawns under drone, get next apple position
	next_pos = measure()

	while next_pos != None:
		start = (get_pos_x(), get_pos_y())
		blocked = get_blocked_positions(path_history, tail_length)

		# Find path to apple
		directions = bfs_find_path(start, next_pos, blocked)

		if directions == None:
			# No path found, we're stuck
			break

		# Follow the path
		stuck = False
		for direction in directions:
			if not move(direction):
				stuck = True
				break
			path_history.append((get_pos_x(), get_pos_y()))

		if stuck:
			break

		# Ate an apple, tail grows
		tail_length = tail_length + 1
		next_pos = measure()

	# Harvest bones by removing hat
	change_hat(Hats.Straw_Hat)


def plant_field(area):
	# For API consistency with other crop modules
	farm_field(area)


def farm(area, amount):
	# Farm bones until we have at least 'amount'
	# Dinosaurs can't use parallel drones (only one hat)
	while num_items(Items.Bone) < amount:
		farm_field(area)
