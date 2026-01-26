import crops

# Global dictionary to keep track of current cost for one crop
current_crop_cost = {}


def order_cost_list(cost_dict):
	ordered_list = []

	order_list = [
		Items.Hay,
		Items.Wood,
		Items.Carrot,
		Items.Pumpkin,
		Items.Cactus,
		Items.Weird_Substance,
		Items.Gold,
		Items.Bone,
	]

	for key in order_list:
		if key in cost_dict:
			ordered_list.append((key, cost_dict[key]))

	return ordered_list


def calculate_items_for_unlock_cost(target_unlock):
	totals = {}

	def expand(item, multiplier=1):
		cost = get_cost(item)

		if cost != None:
			new_cost = {}
			for k in cost:
				new_cost[k] = cost[k]
			current_crop_cost[item] = new_cost

		# Base item or maxed unlock
		if cost == None:
			return

		for sub_item in cost:
			amount = cost[sub_item] * multiplier

			if sub_item in totals:
				totals[sub_item] += amount
			else:
				totals[sub_item] = amount

			if sub_item in crops.entity_for_item:
				expand(crops.entity_for_item[sub_item], amount)

	expand(target_unlock)
	return order_cost_list(totals)


def calculate_remaining_cost(target_unlock):
	# Returns only items we still need (subtracts current inventory)
	costs = calculate_items_for_unlock_cost(target_unlock)
	remaining = []
	for i in range(len(costs)):
		item, amount = costs[i]
		current = num_items(item)
		needed = amount - current
		if needed > 0:
			remaining.append((item, needed))
	return remaining
