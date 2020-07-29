#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Challenges a player to a random battle when PM'd, or accepts any
random battle challenge and runs the battles with other files
in this repo. Partially stolen from showdown.py examples
"""
import showdown
import logging
import asyncio
from pprint import pprint
from battle_manager import Gen1Knight

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open('./data/login.txt', 'rt') as f,\
     open('./data/gen_1_team.txt', 'rt') as team1,\
     open('./data/mono-ghost.txt', 'rt') as team2:
    gen_1_team = team1.read()
    ghost_team = team2.read()
    username, password = f.read().strip().splitlines()

class ChallengeClient(showdown.Client):
    async def on_connect(self):
        self.warriors = dict()
        await self.join('lobby')

    async def on_private_message(self, pm):
        if pm.recipient == self:
            await self.cancel_challenge()
            await asyncio.sleep(1)
            await pm.author.challenge('', 'gen1randombattle')

    async def on_challenge_update(self, challenge_data):
        incoming = challenge_data.get('challengesFrom', {})
        for user, tier in incoming.items():
            if 'random' in tier:
                await self.accept_challenge(user, 'null')
            elif 'gen1ou' in tier:
                await self.accept_challenge(user, gen_1_team)
            elif 'gen7monotype' in tier:
                await self.accept_challenge(user, ghost_team)
            else:
                await self.reject_challenge(user)

    async def on_room_init(self, room_obj):
        if room_obj.id.startswith('battle-'):
            if not 'gen1randombattle' in room_obj.id:
                await asyncio.sleep(3)
                await room_obj.say('Actually, you know what?')
                await asyncio.sleep(2)
                await room_obj.say('I don\'t love this meta. Let\'s try a gen 1 random battle.')
                await room_obj.forfeit()
                await room_obj.leave()
            else:
                self.warriors[room_obj.id] = Gen1Knight(room_obj, self.name)
                await asyncio.sleep(600)
                await room_obj.say('I gotta run.')
                await room_obj.forfeit()

    async def on_receive(self, room_id, inp_type, params):
        if room_id.startswith('battle-'):
            print(inp_type)
            print(params)
            print('')
            if inp_type == 'request' and params != [''] and not '{"wait":' in params[0]:
                self.warriors[room_id].update_team(params)
            if inp_type == 'switch' and 'p2' in params[0]:
                self.warriors[room_id].update_opp(params)
            if inp_type == 'turn' or (inp_type == 'faint' and 'p1' in params[0]) or inp_type == 'error':
                await self.warriors[room_id].next_move(inp_type == 'faint' and 'p1' in params[0])
            if inp_type == 'win':
                await self.warriors[room_id].end_words(params)
                await self.warriors[room_id].room_obj.leave()

ChallengeClient(name=username, password=password, strict_exceptions=True).start()
