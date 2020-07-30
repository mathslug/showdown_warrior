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

	def get_next_move(self, is_forced_switch):
		usable_mons = self.__get_usable_mons()
		usable_moves = self.__get_usable_moves()
		will_switch = self.__get_will_switch(is_forced_switch, usable_mons)
		if will_switch:
			return will_switch, self.__get_next_mon(usable_mons)
		else:
			return will_switch, self.__get_next_attack(usable_moves)

	def __get_usable_mons(self):
		mons_switchable_list = map(lambda mon: not 'fnt' in mon['condition'] and not mon['active'], self.pokemon_list)
		usable_mons = list(compress(map(lambda mon: mon['ident'][4:], self.pokemon_list), mons_switchable_list))
		return usable_mons

	def __get_usable_moves(self):
		moves_selectable_list = map(lambda move: not 'pp' in move.keys() or move['pp'] !=  0, self.active_moves_list)
		usable_moves = list(compress(map(lambda move: move['id'], self.active_moves_list), moves_selectable_list))
		return usable_moves

	def __get_will_switch(self, is_forced_switch, usable_mons):
		if is_forced_switch:
			return True
		elif not usable_mons:
			return False
		else:
			return random.choice([True, False, False, False, False, False, False])

	def __get_next_mon(self, usable_mons):
		return str(random.choice(usable_mons))

	def __get_next_attack(self, usable_moves):
		return str(random.choice(usable_moves))
