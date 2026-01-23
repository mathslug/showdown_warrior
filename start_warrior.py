#!/usr/bin/env python3
import asyncio
import logging
import sys
from os import path
from warrior_player import Gen1WarriorPlayer

async def main():
    log_level = logging.DEBUG if '--debug' in sys.argv else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s | %(message)s',
        datefmt='%H:%M:%S',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('./data/warrior.log'),
        ]
    )

    if path.exists('./data/login.txt'):
        with open('./data/login.txt', 'rt') as f:
            username, password = f.read().strip().splitlines()
    else:
        raise Exception('No credentials saved in data directory.')

    print(f"Starting as {username}...")
    player = Gen1WarriorPlayer(
        username=username,
        password=password,
        training_mode='--train' in sys.argv,
        log_level=log_level,
    )

    if '--rando' in sys.argv:
        await player.ladder(n_games=100)
    else:
        print("Waiting for challenges...")
        await player.accept_challenges(opponent=None, n_challenges=100)

if __name__ == "__main__":
    asyncio.run(main())
