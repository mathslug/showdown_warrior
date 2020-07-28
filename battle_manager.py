#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to run the gen1 pokemon battle.
Mostly in a different file to make it easier to work on.
"""
import pandas as pd
import random
import showdown
from thinker import Gen1Thinker

class Gen1Knight():
    def __init__(self, room_obj):
        self.room_obj = room_obj
        self.big_brain = Gen1Thinker()

    def first_move(self, team):
        my_action = self.big_brain.first_move(team)
        return self.interpret_big_brain(my_action)

    def next_move(self, team, prev_opp_action):
        my_action = self.big_brain.next_move(team, prev_opp_action)
        return self.interpret_big_brain(my_action)

    def interpret_big_brain(self, brain_move):
        if 'a' == brain_move[0]:
            return self.room_obj.move(brain_move[1:])
        elif 's' == brain_move[0]:
            return self.room_obj.switch(brain_move[1:])
