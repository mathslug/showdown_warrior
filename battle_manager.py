#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to run the gen1 pokemon battle.
"""
import asyncio
import json
from thinker import Gen1Thinker

class Gen1Knight():
    def __init__(self, room_obj, username):
        self.room_obj = room_obj
        self.__big_brain = Gen1Thinker()
        self.__username = username

    def process_incoming(self, inp_type, params):
        print(inp_type)
        print(params)
        print('')

        if inp_type == 'request' and params != [''] and not '{"wait":' in params[0]:
            params_dict = json.loads(params[0])
            self.__update_team(params_dict)
            is_forced_switch, is_forced_stay = self.__is_forced_stay_or_switch(params_dict)
            return self.__next_move(is_forced_switch, is_forced_stay)
        elif inp_type in ['switch', 'damage'] and 'p2' in params[0]:
            self.__switch_update_opp_mons(params[0][5:], params[-1])
            return asyncio.sleep(0)
        elif inp_type == 'move' and 'p2' in params[0]:
            self.__move_update_opp_mons(params[1])
            return asyncio.sleep(0)
        elif inp_type == 'win':
            return self.__end_words(params)
        else:
            return asyncio.sleep(0)

    def __is_forced_stay_or_switch(self, params_dict):
        if 'forceSwitch' in params_dict.keys():
            is_forced_switch = True
            is_forced_stay = False
        elif len(params_dict['active']) > 1 and params_dict['active'][1] == '"trapped":true':
            is_forced_switch = False
            is_forced_stay = True
        else:
            is_forced_switch = False
            is_forced_stay = False
        return is_forced_switch, is_forced_stay

    def __update_team(self, team_dict):
        if 'active' in team_dict.keys():
            self.__big_brain.active_moves_list = team_dict['active'][0]['moves']
        self.__big_brain.pokemon_list = team_dict['side']['pokemon']

    def __switch_update_opp_mons(self, opp_mon_id, opp_mon_health_str):
        if opp_mon_id in self.__big_brain.opp_pokemon_dict.keys():
            opp_single_pokemon_dict = self.__big_brain.opp_pokemon_dict[opp_mon_id]
        else:
            opp_single_pokemon_dict = dict()

        if 'fnt' in opp_mon_health_str:
            opp_single_pokemon_dict['health'] = 0
            opp_single_pokemon_dict['status'] = 'fnt'
        else:
            opp_mon_health_list = opp_mon_health_str.split('/')
            opp_single_pokemon_dict['health'] = int(opp_mon_health_list[0])
            opp_mon_health_list_partial = opp_mon_health_list[1].split(' ')
            opp_single_pokemon_dict['max_health'] = int(opp_mon_health_list_partial[0])
            if len(opp_mon_health_list_partial) > 1:
                opp_single_pokemon_dict['status'] = opp_mon_health_list_partial[1]
            else:
                opp_single_pokemon_dict['status'] = 'ok'
        self.__big_brain.opp_active_mon = opp_mon_id
        self.__big_brain.opp_pokemon_dict[opp_mon_id] = opp_single_pokemon_dict

    def __move_update_opp_mons(self, opp_move):
        opp_single_pokemon_dict = self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon]
        if 'moves' in opp_single_pokemon_dict.keys():
            move_list = opp_single_pokemon_dict['moves']
            if not opp_move in move_list:
                move_list.append(opp_move)
                opp_single_pokemon_dict['moves'] = move_list
        else:
            opp_single_pokemon_dict['moves'] = [opp_move]
        self.__big_brain.opp_pokemon_dict[self.__big_brain.opp_active_mon] = opp_single_pokemon_dict

    def __next_move(self, is_forced_switch, is_forced_stay):
        do_switch, my_selection = self.__big_brain.get_next_move(is_forced_switch, is_forced_stay)
        if do_switch:
            return self.room_obj.switch(my_selection)
        else:
            return self.room_obj.move(my_selection)

    def __end_words(self, winner_list):
        winner = winner_list[0]
        if winner == self.__username:
            return self.room_obj.say('gg!')
        else:
            return self.room_obj.say('gg')
