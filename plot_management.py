import hats

import hay
import trees
import carrots
import pumpkins
import weird_substance
import gold
import sunflowers
import cactus
import dinosaurs


# Maps items to their farm functions
farm_func_for_item = {
	Items.Power: sunflowers.farm,
	Items.Hay: hay.farm,
	Items.Wood: trees.farm,
	Items.Carrot: carrots.farm,
	Items.Pumpkin: pumpkins.farm,
	Items.Cactus: cactus.farm,
	Items.Weird_Substance: weird_substance.farm,
	Items.Gold: gold.farm,
	Items.Bone: dinosaurs.farm,
}


def auto_plotter(area, amount_wanted):
	quick_print("-------------")
	for i in range(len(amount_wanted)):
		item, amount = amount_wanted[i]
		current_value = num_items(item)
		quick_print(item, amount, current_value)

	for i in range(len(amount_wanted)):
		item, amount = amount_wanted[i]

		if num_items(item) >= amount:
			continue

		change_hat(hats.hat_for_item[item])

		# Call the farm function for this item
		farm_func = farm_func_for_item[item]
		farm_func(area, amount)
