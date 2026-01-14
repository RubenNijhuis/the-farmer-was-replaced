def generate_coords_from_area(pos, size, mode="NORMAL"):
	if mode == "SNAKE":
		return generate_snake_coords(pos, size)
	elif mode == "NORMAL":
		return generate_grid_coords(pos, size)
	else:
		print("Unknown coordinate mode given ", mode)
		return

def generate_grid_coords(pos, size):
	x, y = pos
	w, h = size
	coords = []

	for row in range(h):
		for col in range(w):
			coords.append((x + col, y + row))

	return coords
	

def generate_snake_coords(pos, size):
	x, y = pos
	w, h = size
	coords = []

	for row in range(h):
		# even rows: left → right
		if row % 2 == 0:
			for col in range(w):
				coords.append((x + col, y + row))
		# odd rows: right → left
		else:
			for col in range(w - 1, -1, -1):
				coords.append((x + col, y + row))

	return coords