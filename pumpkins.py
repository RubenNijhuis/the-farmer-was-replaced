import movement
import utils
import crops

def plant_pumpkin_field(pos, size):
	replant_record = utils.generate_snake_coords(pos, size)

	while replant_record:
		next_round = []

	for position in replant_record:
		movement.go_to(position)
		entity = get_entity_type()

		if entity != Entities.Pumpkin:
			crops.plant_crop(Entities.Pumpkin)
			next_round.append(position)
		elif not can_harvest():
			next_round.append(position)

	replant_record = next_round
