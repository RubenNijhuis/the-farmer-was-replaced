import crops

# Global dictionary to keep track of current cost for one crop
current_crop_cost = {}


def get_pumpkin_yield_per_planted():
	# Pumpkin yield: n³ for n < 6, or n² × 6 for n >= 6
	# Planted: n² (full world)
	# Yield per planted = n (for n < 6) or 6 (for n >= 6)
	n = get_world_size()
	if n < 6:
		return n
	return 6


def get_cactus_yield_per_planted():
	# Cactus yield: count² where count = n² (full sorted chain)
	# Yield per planted = n² (for nxn world)
	n = get_world_size()
	return n * n


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

			# For yield-multiplied crops, adjust the expansion multiplier
			if sub_item in crops.entity_for_item:
				entity = crops.entity_for_item[sub_item]
				adjusted_amount = amount

				# Pumpkins: we get n³ or n²×6 from n² planted
				if sub_item == Items.Pumpkin:
					yield_ratio = get_pumpkin_yield_per_planted()
					adjusted_amount = (amount // yield_ratio) + 1

				# Cactus: we get (n²)² from n² planted
				elif sub_item == Items.Cactus:
					yield_ratio = get_cactus_yield_per_planted()
					adjusted_amount = (amount // yield_ratio) + 1

				expand(entity, adjusted_amount)

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
