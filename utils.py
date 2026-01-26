import coordinates


def map_over_area(area, func, mode="SNAKE"):
	coords = coordinates.generate_coords(area, mode)
	for position in coords:
		func(position)
	return


def run_infinite(func):
	while True:
		func()


def create_slices(area, options=None):
	# options = {"workers": n, "direction": "auto"}
	pos, size = area
	x, y = pos
	width, height = size

	workers = max_drones()
	direction = "auto"
	if options:
		if "workers" in options:
			workers = options["workers"]
		if "direction" in options:
			direction = options["direction"]

	slices = []

	if direction == "horizontal":
		n = workers
		if n > width:
			n = width

		for i in range(n):
			x0 = x + (i * width) // n
			x1 = x + ((i + 1) * width) // n
			slices.append(((x0, y), (x1 - x0, height)))

	elif direction == "vertical":
		n = workers
		if n > height:
			n = height

		for i in range(n):
			y0 = y + (i * height) // n
			y1 = y + ((i + 1) * height) // n
			slices.append(((x, y0), (width, y1 - y0)))

	else:
		# Grid mode
		cols = workers
		if cols > width:
			cols = width

		rows = workers // cols
		if rows * cols < workers:
			rows = rows + 1
		if rows > height:
			rows = height

		count = 0
		for r in range(rows):
			y0 = y + (r * height) // rows
			y1 = y + ((r + 1) * height) // rows

			for c in range(cols):
				if count == workers:
					return slices

				x0 = x + (c * width) // cols
				x1 = x + ((c + 1) * width) // cols

				slices.append(((x0, y0), (x1 - x0, y1 - y0)))
				count += 1

	return slices
