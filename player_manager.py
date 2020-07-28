#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example client that challenges a player to
a random battle when PM'd, or accepts any
random battle challenge. Largely stolen from showdown.py examples
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
                self.warriors[room_obj.id] = Gen1Knight(room_obj)
                await self.warriors[room_obj.id].first_move('todo: add team')
                await asyncio.sleep(30)
                await room_obj.forfeit()
                await room_obj.leave()

    async def on_receive(self, room_id, inp_type, params):
        if room_id.startswith('battle-'):
            if inp_type == 'turn' and params != ['1']:
                await self.warriors[room_id].next_move('todo: add team', 'todo: figure out how to add opp action')

ChallengeClient(name=username, password=password, strict_exceptions=True).start()
