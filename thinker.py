#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class that does the decision-making to run the gen1 pokemon battle.
Mostly in a different file to make it easier to work on.
"""
import random
import pandas as pd
from itertools import compress

class Gen1Thinker():
	def __init__(self):
		self.active_moves_list = []
		self.pokemon_list = []
		self.opp_pokemon_list = []

	def next_move(self, is_forced_switch):
		if is_forced_switch:
			attack_or_switch = 's'
		else:
			attack_or_switch = random.choice(['a','s','a','a','a','s','a'])
		if attack_or_switch == 'a':
			#note: breaks for hyperbeam recharge, etc, w/ no pp
			move_pp_list = map(lambda move: move['pp'] !=  0, self.active_moves_list)
			usable_moves = list(compress(map(lambda move: move['id'], self.active_moves_list),move_pp_list))
			select_num = str(random.choice(usable_moves))
		else:
			alive_mons_list = map(lambda mon: not 'fnt' in mon['condition'], self.pokemon_list)
			usable_mons = list(compress(map(lambda mon: mon['ident'][4:], self.pokemon_list),alive_mons_list))
			select_num = str(random.choice(usable_mons))
		print(attack_or_switch + select_num)
		return attack_or_switch + select_num
