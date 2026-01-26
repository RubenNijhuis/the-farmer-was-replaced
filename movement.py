def go_to(pos):
	size = get_world_size()
	x, y = pos

	if not (0 <= x < size and 0 <= y < size):
		print("Coordinates are out of bounds")
		return

	cx, cy = get_pos_x(), get_pos_y()

	dx = (x - cx) % size
	dx_wrap = (cx - x) % size

	if dx <= dx_wrap:
		for _ in range(dx):
			move(East)
	else:
		for _ in range(dx_wrap):
			move(West)

	cx, cy = get_pos_x(), get_pos_y()

	dy = (y - cy) % size
	dy_wrap = (cy - y) % size

	if dy <= dy_wrap:
		for _ in range(dy):
			move(North)
	else:
		for _ in range(dy_wrap):
			move(South)
