def map_over_map(func):
	pos = (0,0)
	area = (get_world_size(), get_world_size())
	map_over_area(func, pos, area)
			
def map_over_area(func, pos, size):
	coords = generate_snake_coords(pos, size)
	for position in coords:
		func(position)
	return
			
def run_infinite(func):
	while True:
		func()

def generate_coords_from_area(pos, size):
	coords = []
	for i in range(size[0]):
		for j in range(size[1]):
			dest_x, dest_y = i + pos[0], j + pos[1]
			coords.append((dest_x, dest_y))
	return coords

def generate_snake_coords(pos, size):
	x, y = pos
	w, h = size
	coords = []

	row = 0
	while row < h:
		col = 0

		# even rows: left → right
		if row % 2 == 0:
			while col < w:
				coords.append((x + col, y + row))
				col += 1

		# odd rows: right → left
		else:
			col = w - 1
			while col >= 0:
				coords.append((x + col, y + row))
				col -= 1

		row += 1

	return coords