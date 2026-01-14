import movement
import utils
import crops

def replant_pumpkins(replant_positions):
	replant_record = []
	
	for position in replant_positions:
		movement.go_to(position)
		entity = get_entity_type()
		
		if entity == Entities.Pumpkin and can_harvest():
			continue
		
		if entity != Entities.Pumpkin:
			crops.plant_crop(Entities.Pumpkin)
			
		replant_record.append((position))
			
	return replant_record

def farm_pumpkin_field(pos, size):
	replant_record = utils.generate_snake_coords(pos, size)
	
	while replant_record:
		replant_record = replant_pumpkins(replant_record)

	movement.go_to(pos)
	harvest()
