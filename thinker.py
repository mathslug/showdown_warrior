#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class that does the decision-making to run the gen1 pokemon battle.
Mostly in a different file to make it easier to work on.
"""
import random
from itertools import compress

class Gen1Thinker():
	def __init__(self):
		self.active_moves_list = []
		self.pokemon_list = []
		self.opp_active_mon = ''
		self.opp_pokemon_list = []

	def next_move(self, is_forced_switch):
		move_pp_list = map(lambda move: not 'pp' in move.keys() or move['pp'] !=  0, self.active_moves_list)
		usable_moves = list(compress(map(lambda move: move['id'], self.active_moves_list),move_pp_list))

		switchable_mons_list = map(lambda mon: not 'fnt' in mon['condition'] and not mon['active'], self.pokemon_list)
		usable_mons = list(compress(map(lambda mon: mon['ident'][4:], self.pokemon_list),switchable_mons_list))

		if is_forced_switch:
			do_switch = True
		elif not usable_mons:
			do_switch = False
		else:
			do_switch = random.choice([True, False, False, False, False, False, False])

		if do_switch:
			my_selection = str(random.choice(usable_mons))
		else:
			my_selection = str(random.choice(usable_moves))

		return do_switch, my_selection
