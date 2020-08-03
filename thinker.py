#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class that does the decision-making to run the gen1 pokemon battle.
Mostly in a different file to make it easier to work on.
"""
import math
import random
import pandas as pd
from os import path
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
		self.__battle_metrics = dict()
		self.__battle_metrics['turn'] = []
		self.__battle_metrics['action'] = []
		self.__battle_metrics['self_hp'] = []
		self.__battle_metrics['opp_hp'] = []
		self.__battle_metrics['outspeed_prob'] = []
		self.__battle_metrics['is_status_move'] = []
		self.__battle_metrics['exp_damage_done'] = []
		self.__battle_metrics['exp_damage_received'] = []
		self.__battle_metrics['predicted_npw_score'] = []

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
		max_npw_score = max(map(lambda d: d['predicted_npw_score'], action_metrics_list))
		is_best_action_list = list(map(lambda d: d['predicted_npw_score'] == max_npw_score, action_metrics_list))
		best_action_metric_list = list(compress(action_metrics_list, is_best_action_list))
		selected_action_metrics = random.choice(action_metrics_list)
		self.__record_single_action(selected_action_metrics)
		return selected_action_metrics['action']

	def __get_action_metrics(self, action):
		metrics_dict  = dict()
		metrics_dict['action'] = action
		metrics_dict['self_hp'] = self.pokemon_dict[self.active_mon]['health'] / self.pokemon_dict[self.active_mon]['max_health']
		metrics_dict['opp_hp'] = self.opp_pokemon_dict[self.opp_active_mon]['health'] / self.opp_pokemon_dict[self.opp_active_mon]['max_health']
		metrics_dict['outspeed_prob'] = self.__get_outspeed_prob(action)
		metrics_dict['is_status_move'] = int(not action[0] and 'category' in gen1_moves_dict[action[1]].keys() and gen1_moves_dict[action[1]]['category'] == 'Status')
		metrics_dict['exp_damage_done'] = self.__get_damage_done(action)
		metrics_dict['exp_damage_received'] = self.__get_damage_received(action)
		# expected damage done incl probability, assume some switch prob? or start with no switch prob
		# expected damage received incl probability - takes into account general type stuff of switches
		# ^ take mon types and all known move types, max min of relevant stats if more than 1
		metrics_dict['predicted_npw_score'] = self.__get_predicted_npw_score(metrics_dict)
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
		# bonus points would be to keep track of enemy probable speed range based on previous moves
		opp_speed = math.floor(((gen1_mons_dict[self.opp_active_mon]['bs']['spe'] + 15) * 2 + 63) * self.opp_pokemon_dict[self.opp_active_mon]['level'] / 100) + 5
		opp_speed *= 1.5 ** self.opp_pokemon_dict[self.opp_active_mon]['stat_mods']['spe']
		opp_speed *= 0.25 ** (self.opp_pokemon_dict[self.opp_active_mon]['status'] == 'par')
		my_speed = self.pokemon_dict[self.active_mon]['stats']['spe']
		my_speed *= 1.5 ** self.pokemon_dict[self.active_mon]['stat_mods']['spe']
		my_speed *= 0.25 ** (self.pokemon_dict[self.active_mon]['status'] == 'par')
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
				return 1

	def __get_damage_done(self, action):
		print('HERE')
		print(self.pokemon_dict)
		if action[0] or gen1_moves_dict[action[1]]['category'] == 'Status':
			damage = 0
		elif action[1] in ['Night Shade', 'Seismic Toss']:
			damage = self.pokemon_dict[self.active_mon]['level']
		else:
			if gen1_moves_dict[action[1]]['type'] in ['Grass', 'Psychic', 'Ice', 'Water', 'Dragon', 'Fire', 'Electric', 'Dark']:
				atk_stat = self.pokemon_dict[self.active_mon]['stats']['spd']
				atk_stat *= 1.5 ** self.pokemon_dict[self.active_mon]['stat_mods']['spd']
				def_stat = math.floor(((gen1_mons_dict[self.opp_active_mon]['bs']['spd'] + 15) * 2 + 63) * self.opp_pokemon_dict[self.opp_active_mon]['level'] / 100) + 5
				def_stat *= 1.5 ** self.opp_pokemon_dict[self.opp_active_mon]['stat_mods']['spd'] * (1 + self.opp_pokemon_dict[self.opp_active_mon]['is_light_screen_up'])
			else:
				atk_stat = self.pokemon_dict[self.active_mon]['stats']['atk']
				atk_stat *= 1.5 ** self.pokemon_dict[self.active_mon]['stat_mods']['atk']
				def_stat = math.floor(((gen1_mons_dict[self.opp_active_mon]['bs']['def'] + 15) * 2 + 63) * self.opp_pokemon_dict[self.opp_active_mon]['level'] / 100) + 5
				def_stat *= 1.5 ** self.opp_pokemon_dict[self.opp_active_mon]['stat_mods']['def'] * (1 + self.opp_pokemon_dict[self.opp_active_mon]['is_reflect_up'])
			damage = ((2 * self.pokemon_dict[self.active_mon]['level'] / 5 + 2) * gen1_moves_dict[action[1]]['bp'] * atk_stat / def_stat / 50 + 2) *\
					236 / 255 *\
					(1 + 0.5 * (gen1_moves_dict[action[1]]['type'] in gen1_mons_dict[self.active_mon]['types'])) *\
					math.prod(list(map(lambda type: type_effectiveness_dict[gen1_moves_dict[action[1]]['type']][type], gen1_mons_dict[self.opp_active_mon]['types'])))
			damage *= 0.75 ** (self.pokemon_dict[self.active_mon]['status'] == 'par')
			damage *= 0.5 ** (self.pokemon_dict[self.active_mon]['is_confused'])
		prob_opp_full_hp = math.floor(((gen1_mons_dict[self.opp_active_mon]['bs']['hp'] + 15) * 2 + 63) * self.opp_pokemon_dict[self.opp_active_mon]['level'] / 100) +\
				self.opp_pokemon_dict[self.opp_active_mon]['level'] + 10
		return min(damage / prob_opp_full_hp, 1)

	def  __get_damage_received(self, action):
		if action[0]:
			expected_mon = action[1]
		else:
			expected_mon = self.active_mon
		if not self.opp_pokemon_dict[self.opp_active_mon]['moves']:
			expected_moves = ['Body Slam']
		else:
			expected_moves = self.opp_pokemon_dict[self.opp_active_mon]['moves']

		# should fix all this and the above to use versatile functions
		damages = []
		for move in expected_moves:
			if gen1_moves_dict[move]['type'] in ['Grass', 'Psychic', 'Ice', 'Water', 'Dragon', 'Fire', 'Electric', 'Dark']:
				atk_stat = math.floor(((gen1_mons_dict[self.opp_active_mon]['bs']['spd'] + 15) * 2 + 63) * self.opp_pokemon_dict[self.opp_active_mon]['level'] / 100) + 5
				atk_stat *= 1.5 ** self.opp_pokemon_dict[self.opp_active_mon]['stat_mods']['spd']
				def_stat = self.pokemon_dict[expected_mon]['stats']['spd']
				def_stat *= 1.5 ** self.pokemon_dict[expected_mon]['stat_mods']['spd'] * (1 + (not action[0] and self.pokemon_dict[expected_mon]['is_light_screen_up']))
			else:
				atk_stat = math.floor(((gen1_mons_dict[self.opp_active_mon]['bs']['atk'] + 15) * 2 + 63) * self.opp_pokemon_dict[self.opp_active_mon]['level'] / 100) + 5
				atk_stat *= 1.5 ** self.opp_pokemon_dict[self.opp_active_mon]['stat_mods']['atk']
				def_stat = self.pokemon_dict[expected_mon]['stats']['def']
				def_stat *= 1.5 ** self.pokemon_dict[expected_mon]['stat_mods']['def'] * (1 + (not action[0] and self.pokemon_dict[expected_mon]['is_reflect_up']))
			damage = ((2 * self.opp_pokemon_dict[self.opp_active_mon]['level'] / 5 + 2) * gen1_moves_dict[move]['bp'] * atk_stat / def_stat / 50 + 2) *\
					236 / 255 *\
					(1 + 0.5 * (gen1_moves_dict[move]['type'] in gen1_mons_dict[self.opp_active_mon]['types'])) *\
					math.prod(list(map(lambda type: type_effectiveness_dict[gen1_moves_dict[move]['type']][type], gen1_mons_dict[expected_mon]['types'])))
			damage *= 0.75 ** (self.opp_pokemon_dict[self.opp_active_mon]['status'] == 'par')
			damage *= 0.5 ** (self.opp_pokemon_dict[self.opp_active_mon]['is_confused'])
			damages.append(damage)
		return max(damages) / self.pokemon_dict[expected_mon]['max_health']

	def __record_single_action(self, metrics_dict):
		self.__battle_metrics['turn'].append(self.turn_counter)
		self.__battle_metrics['action'].append(metrics_dict['action'][1])
		self.__battle_metrics['self_hp'].append(metrics_dict['self_hp'])
		self.__battle_metrics['opp_hp'].append(metrics_dict['opp_hp'])
		self.__battle_metrics['outspeed_prob'].append(metrics_dict['outspeed_prob'])
		self.__battle_metrics['is_status_move'].append(metrics_dict['is_status_move'])
		self.__battle_metrics['exp_damage_done'].append(metrics_dict['exp_damage_done'])
		self.__battle_metrics['exp_damage_received'].append(metrics_dict['exp_damage_received'])
		self.__battle_metrics['predicted_npw_score'].append(metrics_dict['predicted_npw_score'])

	def record_battle(self, knight_wins):
		self.__battle_metrics['actual_npw_score'] = list(map(lambda turn: knight_wins / 1.1 ** (self.turn_counter - turn), self.__battle_metrics['turn']))
		battle_frame = pd.DataFrame.from_dict(self.__battle_metrics)
		# should probably have start_warrior pass this down. idk.
		if path.exists('./data/battle_records.csv'):
			old_battle_frame = pd.read_csv('./data/battle_records.csv')
			battle_frame = old_battle_frame.merge(battle_frame)
		battle_frame.to_csv('./data/battle_records.csv')
