def generate_coords(area, mode="NORMAL"):
	if mode == "SNAKE":
		return generate_snake_coords(area)
	elif mode == "NORMAL":
		return generate_grid_coords(area)
	else:
		print("Unknown coordinate mode given ", mode)
		return


def generate_grid_coords(area):
	pos, size = area
	x, y = pos
	w, h = size
	coords = []

	for row in range(h):
		for col in range(w):
			coords.append((x + col, y + row))

	return coords


def generate_diamond(grid, spacing, options=None):
	# grid = (rows, cols), spacing = (dx, dy), options = {"x_offset_pattern": [...]}
	rows, cols = grid
	dx, dy = spacing
	x_offset_pattern = None
	if options:
		x_offset_pattern = options.get("x_offset_pattern")

	coords = []
	for i in range(rows):
		y = i * dy
		offset = 0
		if x_offset_pattern and i < len(x_offset_pattern):
			offset = x_offset_pattern[i]
		for j in range(cols):
			x = j * dx + offset
			coords.append((x, y))
	return coords


def generate_snake_coords(area):
	pos, size = area
	x, y = pos
	w, h = size
	coords = []

	for row in range(h):
		# even rows: left to right
		if row % 2 == 0:
			for col in range(w):
				coords.append((x + col, y + row))
		# odd rows: right to left
		else:
			for col in range(w - 1, -1, -1):
				coords.append((x + col, y + row))

	return coords
