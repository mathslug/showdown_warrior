#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to run the gen1 pokemon battle.
"""
import showdown
import json
from thinker import Gen1Thinker

class Gen1Knight():
    def __init__(self, room_obj, username):
        self.room_obj = room_obj
        self.big_brain = Gen1Thinker()
        self.username = username

    def update_team(self, team_params):
        team_dict = json.loads(team_params[0])
        if not '{"forceSwitch":' in team_params[0]:
            self.big_brain.active_moves_list = team_dict['active'][0]['moves']
        self.big_brain.pokemon_list = team_dict['side']['pokemon']

    def update_opp(self, opp_params):
        opp_mon = opp_params[1]
        if not opp_mon in self.big_brain.opp_pokemon_list:
            self.big_brain.opp_pokemon_list.append(opp_mon)

    def next_move(self, is_forced_switch):
        my_action = self.big_brain.next_move(is_forced_switch)
        return self.interpret_big_brain(my_action)

    def end_words(self, winner_list):
        winner = winner_list[0]
        if winner == self.username:
            return self.room_obj.say('gg!')
        else:
            return self.room_obj.say('gg')

    def interpret_big_brain(self, brain_move):
        if 'a' == brain_move[0]:
            return self.room_obj.move(brain_move[1:])
        elif 's' == brain_move[0]:
            return self.room_obj.switch(brain_move[1:])
