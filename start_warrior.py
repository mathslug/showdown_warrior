#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run this (python start_warrior.py) to enter lobby,
start accepting challenges, and play battles according to thinker.py.
First consider a virtualenv, then pip install requirements.txt if needed
"""
import logging
from player_manager import ChallengeClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open('./data/login.txt', 'rt') as f,\
     open('./data/gen_1_team.txt', 'rt') as team1,\
     open('./data/mono-ghost.txt', 'rt') as team2:
    gen_1_team = team1.read()
    ghost_team = team2.read()
    username, password = f.read().strip().splitlines()

ChallengeClient(name=username,password=password,strict_exceptions=True).start()
