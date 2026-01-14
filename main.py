import utils
import plot_management

clear()
do_a_flip()

minimum_amounts = {
	Items.Power:			1000000,
	Items.Hay:				10000,
	Items.Wood:				10000,
	Items.Carrot:			10000,
	Items.Pumpkin:			10000,
	Items.Cactus:			10000,
	Items.Weird_Substance:	10000,
	Items.Gold:				10000
}

def main():
	plot_management.auto_plotter(minimum_amounts)

utils.run_infinite(main)