import utils
import movement


def run_in_thread(area, func, slices=None):
	drones = []

	if slices == None:
		slices = utils.create_slices(area)

	for slice in slices:
		slice_pos = slice[0]

		def drone_task():
			return func(slice)

		movement.go_to(slice_pos)
		drone = spawn_drone(drone_task)
		if drone:
			drones.append(drone)
		else:
			drone_task()

	# Wait for all drones to finish
	for drone in drones:
		wait_for(drone)


def run_func(area, func, options=None):
	# options = {"slices": [...], "threaded": True}
	slices = None
	threaded = True
	if options:
		if "slices" in options:
			slices = options["slices"]
		if "threaded" in options:
			threaded = options["threaded"]

	if threaded:
		run_in_thread(area, func, slices)
	else:
		func(area)


def run_func_looped(area, func, slices=None):
	# Spawns drones that loop forever over their slice. Never returns.
	run_func_until(area, func, {"slices": slices})


def run_func_until(area, func, options=None):
	# Spawns drones that loop until should_stop() returns True.
	# options = {"should_stop": func, "slices": [...]}
	# If should_stop not provided, loops forever.
	drones = []

	slices = None
	should_stop = None
	has_stop_condition = False
	if options:
		if "slices" in options:
			slices = options["slices"]
		if "should_stop" in options:
			should_stop = options["should_stop"]
			has_stop_condition = True

	if slices == None:
		slices = utils.create_slices(area)

	for slice in slices:
		slice_pos = slice[0]

		def drone_task():
			if has_stop_condition:
				while not should_stop():
					func(slice)
			else:
				while True:
					func(slice)

		movement.go_to(slice_pos)
		drone = spawn_drone(drone_task)
		if drone:
			drones.append(drone)

	# Main drone also works instead of idling
	main_slice = slices[len(slices) - 1]
	if has_stop_condition:
		while not should_stop():
			func(main_slice)

		# Wait for other drones to finish their current iteration
		for drone in drones:
			wait_for(drone)
	else:
		while True:
			func(main_slice)
