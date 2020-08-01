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
		usable_moves = compress(map(lambda move: move['id'], self.active_moves_list), moves_selectable_list)
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
		# TK: add metrics lol
		metrics_dict['npw_score'] = self.__get_predicted_npw_score(metrics_dict)
		return metrics_dict

	def __get_predicted_npw_score(self, metrics_dict):
		# npw = sqrt(1 / # turns to win)
		# 0 = did not win
		return 0
