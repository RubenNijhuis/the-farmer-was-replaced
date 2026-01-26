filename = "auto_unlock"
sim_unlocks = {}
sim_items = {}
sim_globals = {}
seed = -1
speedup = 100

clear()

run_time = simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)
