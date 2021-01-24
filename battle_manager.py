#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to run the gen1 pokemon battle.
"""
import asyncio
import json
from thinker import Gen1Thinker

class Gen1Knight():
    def __init__(self, room_obj, username, training_mode):
        self.room_obj = room_obj
        self.__big_brain = Gen1Thinker(training_mode)
        self.__username = username
        self.__opp_name = ''
        self.__is_forced_switch = False
        self.__is_forced_stay = False
        self.__player_dict = dict()
        self.__is_catchup_mode = False
        self.__is_faint_move = False

    def process_incoming(self, inp_type, params):
        print(inp_type)
        print(params)
        print('')

        if inp_type == 'request' and params != [''] and not '{"wait":' in params[0]:
            params_dict = json.loads(params[0])
            self.__update_team(params_dict)
            self.__is_forced_switch, self.__is_forced_stay = self.__is_forced_stay_or_switch(params_dict)
        elif inp_type == 'player':
            self.__player_dict[params[1]] = params[0]
            if params[1] != self.__username:
                self.__opp_name = params[1]
        elif inp_type in ['switch', '-damage', '-heal']:
            self.__switch_damage_update_mons(params[0][5:], params[1 + (inp_type == 'switch')], self.__player_dict[self.__opp_name] in params[0], params[1].split(', L'))
        elif inp_type == 'move':
            if self.__player_dict[self.__opp_name] in params[0]:
                self.__move_update_opp_mons(params[1])
            if params[1] == 'Haze':
                self.__haze_reset(self.__player_dict[self.__opp_name] in params[0])
        elif inp_type in ['win', 'tie']:
            return self.__end_words(params)
        elif inp_type == 'turn':
            if int(params[0]) > self.__big_brain.turn_counter:
                self.__big_brain.turn_counter = int(params[0])
                self.__is_catchup_mode = False
                self.__is_faint_move = False
                return self.__next_move()
            elif int(params[0]) == self.__big_brain.turn_counter:
                self.__is_catchup_mode = False
                if not self.__is_faint_move:
                    return self.__next_move()
            else:
                self.__is_catchup_mode = True
        elif inp_type == 'faint' and self.__player_dict[self.__username] in params[0] and not self.__is_catchup_mode:
            self.__is_faint_move = True
            self.__big_brain.pokemon_dict[params[0][5:]]['status'] = 'fnt'
            if list(map(lambda mon: self.__big_brain.pokemon_dict[mon]['status'], self.__big_brain.pokemon_dict.keys())).count('fnt') < 6:
                return self.__next_move()
        elif inp_type == 'error':
            print('ERROR, RE-CHOOSING')
            return self.__next_move()
        elif inp_type == '-status' and self.__player_dict[self.__opp_name] in params[0]:
            self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]['status'] = params[1]
        elif (inp_type == '-boost') and params[1] != 'spa':
            if params[0].split('a: ')[0] == self.__player_dict[self.__username]:
                self.__big_brain.pokemon_dict[self.__big_brain.active_mon]['stat_mods'][params[1]] += int(params[2])
            elif params[0].split('a: ')[0] == self.__player_dict[self.__opp_name]:
                self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]['stat_mods'][params[1]] += int(params[2])
            else:
                raise Exception('boost allocation error: ' + inp_type + params[0] + params[1] + params[2])
        elif (inp_type == '-unboost') and params[1] != 'spa':
            if params[0].split('a: ')[0] == self.__player_dict[self.__username]:
                self.__big_brain.pokemon_dict[self.__big_brain.active_mon]['stat_mods'][params[1]] -= int(params[2])
            elif params[0].split('a: ')[0] == self.__player_dict[self.__opp_name]:
                self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]['stat_mods'][params[1]] -= int(params[2])
            else:
                raise Exception('boost allocation error: ' + inp_type + params[0] + params[1] + params[2])
        elif inp_type == '-start':
            if params[1] == 'Reflect':
                if self.__player_dict[self.__username] in params[0]:
                    self.__big_brain.pokemon_dict[self.__big_brain.active_mon]['is_reflect_up'] = True
                else:
                    self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]['is_reflect_up'] = True
            if 'creen' in params[1]:
                if self.__player_dict[self.__username] in params[0]:
                    self.__big_brain.pokemon_dict[self.__big_brain.active_mon]['is_light_screen_up'] = True
                else:
                    self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]['is_light_screen_up'] = True
            if params[1] == 'confusion':
                if self.__player_dict[self.__username] in params[0]:
                    self.__big_brain.pokemon_dict[self.__big_brain.active_mon]['is_confused'] = True
                else:
                    self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]['is_confused'] = True
        elif inp_type == '-end' and params[1] == 'confusion':
            if self.__player_dict[self.__username] in params[0]:
                self.__big_brain.pokemon_dict[self.__big_brain.active_mon]['is_confused'] = False
            else:
                self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]['is_confused'] = False
        return asyncio.sleep(0)

    def __is_forced_stay_or_switch(self, params_dict):
        if 'forceSwitch' in params_dict.keys():
            is_forced_switch = True
            is_forced_stay = False
        elif 'trapped' in params_dict['active'][0].keys() and params_dict['active'][0]['trapped']:
            is_forced_switch = False
            is_forced_stay = True
        else:
            is_forced_switch = False
            is_forced_stay = False
        return is_forced_switch, is_forced_stay

    def __update_team(self, team_dict):
        if 'active' in team_dict.keys():
            self.__big_brain.active_moves_list = team_dict['active'][0]['moves']
        pokemon_list = team_dict['side']['pokemon']
        pokemon_dict = dict()
        active_mon_id = ''
        for mon in pokemon_list:
            mon_id = mon['ident'][4:]
            single_pokemon_dict = dict()
            single_pokemon_dict['active'] = mon['active']
            if self.__big_brain.turn_counter == 0:
                single_pokemon_dict['is_confused'] = False
                single_pokemon_dict['is_reflect_up'] = False
                single_pokemon_dict['is_light_screen_up'] = False
                single_pokemon_dict['stat_mods'] = dict()
                single_pokemon_dict['stat_mods']['atk'] = 0
                single_pokemon_dict['stat_mods']['def'] = 0
                single_pokemon_dict['stat_mods']['spe'] = 0
                single_pokemon_dict['stat_mods']['spd'] = 0
                single_pokemon_dict['stat_mods']['accuracy'] = 0
                single_pokemon_dict['stat_mods']['evasion'] = 0
            else:
                single_pokemon_dict['stat_mods'] = self.__big_brain.pokemon_dict[mon_id]['stat_mods']
                single_pokemon_dict['is_confused'] = self.__big_brain.pokemon_dict[mon_id]['is_confused']
                single_pokemon_dict['is_reflect_up'] = self.__big_brain.pokemon_dict[mon_id]['is_reflect_up']
                single_pokemon_dict['is_light_screen_up'] = self.__big_brain.pokemon_dict[mon_id]['is_light_screen_up']
            if single_pokemon_dict['active']:
                active_mon_id = mon_id
            mon_health_str = mon['condition']
            if 'fnt' in mon_health_str:
                single_pokemon_dict['health'] = 0
                single_pokemon_dict['max_health'] = self.__big_brain.pokemon_dict[mon_id]['max_health']
                single_pokemon_dict['status'] = 'fnt'
            else:
                mon_health_list = mon_health_str.split('/')
                single_pokemon_dict['health'] = int(mon_health_list[0])
                mon_health_list_partial = mon_health_list[1].split(' ')
                single_pokemon_dict['max_health'] = int(mon_health_list_partial[0])
                if len(mon_health_list_partial) > 1:
                    single_pokemon_dict['status'] = mon_health_list_partial[1]
                else:
                    single_pokemon_dict['status'] = 'ok'
            single_pokemon_dict['moves'] = mon['moves']
            single_pokemon_dict['stats'] = mon['stats']
            del single_pokemon_dict['stats']['spa']
            single_pokemon_dict['level'] = int(mon['details'].split(', L')[1])
            pokemon_dict[mon_id] = single_pokemon_dict
        self.__big_brain.active_mon = active_mon_id
        self.__big_brain.pokemon_dict = pokemon_dict


    def __switch_damage_update_mons(self, mon_id, mon_health_str, is_opp_mon, level_param_list):
        if is_opp_mon and mon_id in self.__big_brain.opp_pokemon_dict.keys():
            single_pokemon_dict = self.__big_brain.opp_pokemon_dict[mon_id]
        elif not is_opp_mon and mon_id in self.__big_brain.pokemon_dict.keys():
            single_pokemon_dict = self.__big_brain.pokemon_dict[mon_id]
        else:
            single_pokemon_dict = dict()
            single_pokemon_dict['moves'] = []

        if len(level_param_list) > 1: # is it a switch
            single_pokemon_dict['level'] = int(level_param_list[1])
            # for now just reset on switch IN bc easier
            single_pokemon_dict['is_confused'] = False
            single_pokemon_dict['is_reflect_up'] = False
            single_pokemon_dict['is_light_screen_up'] = False
            single_pokemon_dict['stat_mods'] = dict()
            single_pokemon_dict['stat_mods']['atk'] = 0
            single_pokemon_dict['stat_mods']['def'] = 0
            single_pokemon_dict['stat_mods']['spe'] = 0
            single_pokemon_dict['stat_mods']['spd'] = 0
            single_pokemon_dict['stat_mods']['accuracy'] = 0
            single_pokemon_dict['stat_mods']['evasion'] = 0

        if 'fnt' in mon_health_str:
            single_pokemon_dict['health'] = 0
            single_pokemon_dict['status'] = 'fnt'
        else:
            mon_health_list = mon_health_str.split('/')
            single_pokemon_dict['health'] = int(mon_health_list[0])
            mon_health_list_partial = mon_health_list[1].split(' ')
            single_pokemon_dict['max_health'] = int(mon_health_list_partial[0])
            if len(mon_health_list_partial) > 1:
                single_pokemon_dict['status'] = mon_health_list_partial[1]
            else:
                single_pokemon_dict['status'] = 'ok'
        if is_opp_mon:
            self.__big_brain.opp_active_mon = mon_id
            self.__big_brain.opp_pokemon_dict[mon_id] = single_pokemon_dict
        else:
            self.__big_brain.active_mon = mon_id
            self.__big_brain.pokemon_dict[mon_id] = single_pokemon_dict

    def __move_update_opp_mons(self, opp_move):
        opp_single_pokemon_dict = self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]
        move_list = opp_single_pokemon_dict['moves']
        if not opp_move in move_list:
            move_list.append(opp_move)
            opp_single_pokemon_dict['moves'] = move_list
        self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon] = opp_single_pokemon_dict

    def __next_move(self):
        do_switch, my_selection = self.__big_brain.get_next_move(self.__is_forced_switch, self.__is_forced_stay)
        if do_switch:
            return self.room_obj.switch(my_selection)
        else:
            return self.room_obj.move(my_selection)

    def __end_words(self, winner_list):
        if winner_list == []:
            is_tie = True
            knight_wins = True
        else:
            is_tie = False
            knight_wins = winner_list[0] == self.__username
        self.__big_brain.record_battle(is_tie, knight_wins)
        if knight_wins:
            return self.room_obj.say('gg!')
        else:
            return self.room_obj.say('gg')

    def  __haze_reset(self, is_user_opp):
        if is_user_opp:
            self.__big_brain.pokemon_dict[self.__big_brain.active_mon]['status'] = 'ok'
        else:
            self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]['status'] = 'ok'
        for single_pokemon_dict in [self.__big_brain.pokemon_dict[self.__big_brain.active_mon],  self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]]:
            single_pokemon_dict['is_confused'] = False
            single_pokemon_dict['is_reflect_up'] = False
            single_pokemon_dict['is_light_screen_up'] = False
            single_pokemon_dict['stat_mods']['atk'] = 0
            single_pokemon_dict['stat_mods']['def'] = 0
            single_pokemon_dict['stat_mods']['spe'] = 0
            single_pokemon_dict['stat_mods']['spd'] = 0
            single_pokemon_dict['stat_mods']['accuracy'] = 0
            single_pokemon_dict['stat_mods']['evasion'] = 0
