#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run this (python start_warrior.py) to enter lobby,
start accepting challenges, and play battles according to thinker.py.
First consider a virtualenv, then pip install requirements.txt if needed.
"""
import logging
from os import path
from player_manager import ChallengeClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if path.exists('./data/login.txt'):
    with open('./data/login.txt', 'rt') as f:
        username, password = f.read().strip().splitlines()
else:
    raise Exception('No credentials saved in data directory.')

ChallengeClient(name=username,
                password=password,
                strict_exceptions=True).start()
                #strict_exceptions=True).start(autoreconnect=True)
