#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Challenges a player to a random battle when PM'd, or accepts any
random battle challenge and runs the battles with other files
in this repo. Partially stolen from showdown.py examples
"""
import showdown
import asyncio
from pprint import pprint
from battle_manager import Gen1Knight
from os import path

class ChallengeClient(showdown.Client):
    def __init__(self, training_mode, *args, **kwargs):
        super(ChallengeClient, self).__init__(*args, **kwargs)
        self.training_mode = training_mode
        self.warriors = dict()
        self.gen_1_team = ''
        self.ghost_team = ''
        if path.exists('./data/gen_1_team.txt'):
            with open('./data/gen_1_team.txt', 'rt') as team1:
                self.gen_1_team = team1.read()
        if path.exists('./data/mono-ghost.txt'):
            with open('./data/mono-ghost.txt', 'rt') as team2:
                self.ghost_team = team2.read()


    async def on_connect(self):
        await self.join('lobby')
        await asyncio.sleep(5)

        # in case of autoreconnect, resend last move
        for room_id in self.warriors.keys():
            await self.join(room_id)

        #uncomment below line to start searching on login
        #await self.search_battles('', 'gen1randombattle')

        #uncomment below line to message user XX on init
        #await self.private_message('XX', 'hello there')

        #uncomment below lines to run for 2 hours and then quit, also comment out room deinit
        #await asyncio.sleep(7200)
        #quit()

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
            elif 'gen1ou' in tier and self.gen_1_team:
                await self.accept_challenge(user, self.gen_1_team)
            elif 'gen7monotype' in tier and self.ghost_team:
                await self.accept_challenge(user, self.ghost_team)
            else:
                await self.reject_challenge(user)

    async def on_room_init(self, room_obj):
        if room_obj.id.startswith('battle-'):
            if not 'gen1randombattle' in room_obj.id:
                await asyncio.sleep(3)
                await room_obj.say('Actually, you know what?')
                await asyncio.sleep(2)
                await room_obj.say('I don\'t love this meta.')
                await asyncio.sleep(1)
                await room_obj.say('Let\'s try a gen 1 random battle.')
                await room_obj.forfeit()
                await room_obj.leave()
            else:
                if room_obj.id not in self.warriors.keys():
                    self.warriors[room_obj.id] = Gen1Knight(room_obj, self.name, self.training_mode)
                # don't stay in any room longer than 15 minutes
                await asyncio.sleep(900)
                await room_obj.say('I gotta run.')
                await room_obj.forfeit()

    async def on_receive(self, room_id, inp_type, params):
        if room_id in self.warriors.keys():
            await self.warriors[room_id].process_incoming(inp_type, params)
            if inp_type == 'win':
                await self.warriors[room_id].room_obj.leave()

    async def on_room_deinit(self, room_obj):
        user_inp = input('Do another battle / stay online (y/n)?').lower()
        if user_inp == 'y':
            await asyncio.sleep(0)

            #uncomment below to play another random battle on battle end
            #await self.search_battles('', 'gen1randombattle')

            #uncomment below line to message user XX on battle end
            #await self.private_message('XX', 'hello there')
        else:
            await asyncio.sleep(0)
            quit()
