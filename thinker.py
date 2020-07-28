#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class that does the decision-making to run the gen1 pokemon battle.
Mostly in a different file to make it easier to work on.
"""
import pandas as pd
import random

class Gen1Thinker():
	def __init__(self):
		self.self_actions = []
		self.opp_actions = []

	def first_move(self, team):
		my_action = random.choice(['a1','s2','a2','s3','a3','a4'])
		self.self_actions.append(my_action)
		return my_action

	def next_move(self, team, prev_opp_action):
		action_df = pd.DataFrame([self.self_actions, self.opp_actions]).transpose()
		action_df.columns=['us','them']
		# use the above df to somehow decide what move to do lol
		my_action = random.choice(['a1','s2','a2','s3','a3','a4'])
		self.self_actions.append(my_action)
		return my_action
