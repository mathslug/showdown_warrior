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
            return self.__next_move('forceSwitch' in params_dict.keys())
        elif inp_type == 'switch' and 'p2' in params[0]:
            self.__update_opp_mons(params)
            return asyncio.sleep(0)
        elif inp_type == 'win':
            return self.__end_words(params)
        else:
            return asyncio.sleep(0)

    def __update_team(self, team_dict):
        if 'active' in team_dict.keys():
            self.__big_brain.active_moves_list = team_dict['active'][0]['moves']
        self.__big_brain.pokemon_list = team_dict['side']['pokemon']

    def __update_opp_mons(self, opp_params):
        opp_mon = opp_params[1]
        self.__big_brain.opp_active_mon = opp_mon
        if not opp_mon in self.__big_brain.opp_pokemon_list:
            self.__big_brain.opp_pokemon_list.append(opp_mon)

    def __next_move(self, is_forced_switch):
        do_switch, my_selection = self.__big_brain.get_next_move(is_forced_switch)
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
