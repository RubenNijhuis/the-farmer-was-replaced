import coordinates

def map_over_area(func, pos, size, mode):
	coords = coordinates.generate_coords_from_area(pos, size, mode)
	for position in coords:
		func(position)
	return

def run_infinite(func):
	while True:
		func()