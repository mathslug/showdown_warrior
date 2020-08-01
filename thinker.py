#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class that does the decision-making to run the gen1 pokemon battle.
Mostly in a different file to make it easier to work on.
"""
import math
import random
from itertools import compress
from general_poke_data import *

class Gen1Thinker():
	def __init__(self):
		self.turn_counter = 0
		self.active_mon = ''
		self.active_moves_list = []
		self.pokemon_dict = dict()
		self.opp_active_mon = ''
		self.opp_pokemon_dict = dict()

	def get_next_move(self, is_forced_switch, is_forced_stay):
		actions = self.__get_possible_actions(is_forced_switch, is_forced_stay)
		selection = self.__choose_next_action(actions)
		return selection

	def __get_possible_actions(self, is_forced_switch, is_forced_stay):
		moves_selectable_list = map(lambda move: not 'pp' in move.keys() or move['pp'] !=  0 and not is_forced_switch, self.active_moves_list)
		usable_moves = compress(map(lambda move: move['move'], self.active_moves_list), moves_selectable_list)
		usable_moves = map(lambda move: [False, move], usable_moves)

		mons_switchable_list = map(lambda key: 'fnt' != self.pokemon_dict[key]['status'] and not self.pokemon_dict[key]['active'] and not is_forced_stay, self.pokemon_dict.keys())
		usable_mons = compress(self.pokemon_dict.keys(), mons_switchable_list)
		usable_mons =  map(lambda mon: [True, mon], usable_mons)

		return list(usable_mons) + list(usable_moves)

	def __choose_next_action(self, actions):
		action_metrics_list = list(map(self.__get_action_metrics, actions))
		max_npw_score = max(map(lambda d: d['npw_score'], action_metrics_list))
		is_best_action_list = list(map(lambda d: d['npw_score'] == max_npw_score, action_metrics_list))
		best_action_list = list(compress(actions, is_best_action_list))
		return random.choice(best_action_list)

	def __get_action_metrics(self, action):
		metrics_dict = dict()
		metrics_dict['action'] = action
		print('USE')
		print(self.opp_pokemon_dict)
		metrics_dict['self_hp'] = self.pokemon_dict[self.active_mon]['health'] / self.pokemon_dict[self.active_mon]['max_health']
		metrics_dict['opp_hp'] = self.opp_pokemon_dict[self.opp_active_mon]['health'] / self.opp_pokemon_dict[self.opp_active_mon]['max_health']
		metrics_dict['outspeed_prob'] = self.__get_outspeed_prob(action)
		metrics_dict['is_status_move'] = int(not action[0] and 'category' in gen1_moves_dict[action[1]].keys() and gen1_moves_dict[action[1]]['category'] == 'Status')
		# expected damage done incl probability, assume some switch prob? or start with no switch prob
		# expected damage received incl probability - takes into account general type stuff of switches
		# ^ take mon types and all known move types, max min of relevant stats if more than 1
		metrics_dict['npw_score'] = self.__get_predicted_npw_score(metrics_dict)
		return metrics_dict

	def __get_predicted_npw_score(self, metrics_dict):
		# npw = sqrt(1 / # turns to win)
		#or, more like npv, npw = 1 / (1.1)^turns to win, replace 1.2 with something to make avg win time ~ .5
		# 0 = did not win
		return 0

	def __get_outspeed_prob(self, action):
		if action[0] or action[1] == 'Quick Attack':
			return 1
		elif action[1] == 'Counter':
			return 0
		# assume EVs and IVs maxed out bc no reason for them not to be
		opp_speed = math.floor(((gen1_mons_dict[self.opp_active_mon]['bs']['spe'] + 15) * 2 + 63) * self.opp_pokemon_dict[self.opp_active_mon]['level'] / 100) + 5
		opp_speed *= 1.5 ** self.opp_pokemon_dict[self.opp_active_mon]['stat_mods']['spe']
		my_speed = self.pokemon_dict[self.active_mon]['stats']['spe']
		my_speed *= 1.5 ** self.pokemon_dict[self.active_mon]['stat_mods']['spe']
		if opp_speed > my_speed:
			if 'Counter' in self.opp_pokemon_dict[self.opp_active_mon]['moves']:
				return 0.25
			else:
				return 0
		elif opp_speed == my_speed:
			if 'Counter' in self.opp_pokemon_dict[self.opp_active_mon]['moves'] and 'Quick Attack' in self.opp_pokemon_dict[self.opp_active_mon]['moves']:
				return 0.5
			elif 'Counter' in self.opp_pokemon_dict[self.opp_active_mon]['moves']:
				return 0.375
			elif 'Quick Attack' in self.opp_pokemon_dict[self.opp_active_mon]['moves']:
				return 0.625
			else:
				return 0.5
		else:
			if 'Quick Attack' in self.opp_pokemon_dict[self.opp_active_mon]['moves']:
				return 0.75
			else:
				return 0
