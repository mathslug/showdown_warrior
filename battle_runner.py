#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example client that challenges a player to 
a random battle when PM'd, or accepts any
random battle challenge. Mostly stolen from showdown.py examples
"""
import showdown
import logging
import asyncio
from pprint import pprint
from player import Gen1Player

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
        await self.join('lobby')

    async def on_private_message(self, pm):
        if pm.recipient == self:
            await self.cancel_challenge()
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
                big_brain = Gen1Player()
                first_move = big_brain.first_move('todo: add team')
                await self.interpret_big_brain(first_move, room_obj)
                await asyncio.sleep(30)
                await room_obj.forfeit()
                await room_obj.leave()

    def interpret_big_brain(self, brain_move, room):
        if 'a' == brain_move[0]:
            return room.move(brain_move[1:])
        elif 's' == brain_move[0]:
            return room.switch(brain_move[1:])

ChallengeClient(name=username, password=password).start()
