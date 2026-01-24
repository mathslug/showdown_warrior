#!/usr/bin/env python3
"""
Entry point for the Gen 1 Pokemon Battle Warrior.

Usage:
    python start_warrior.py [options]

Options:
    --local             Connect to local Pokemon Showdown server
    --train             Enable training mode (manual move selection)
    --debug             Enable debug logging
    --rando             Search for random battles on ladder
    --challenge NAME    Challenge a specific player
    --method METHOD     ML method to use (knn, gb). Default: knn
    -c, --credentials   Path to credentials file (default: ./data/login.txt)
"""
import asyncio
import logging
import sys
from os import path

from warrior_player import Gen1WarriorPlayer
from poke_env.ps_client.server_configuration import LocalhostServerConfiguration


async def main():
    # Configure logging
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

    # Get credentials file path
    credentials_file = './data/login.txt'
    if '--credentials' in sys.argv:
        idx = sys.argv.index('--credentials')
        if idx + 1 < len(sys.argv):
            credentials_file = sys.argv[idx + 1]
    elif '-c' in sys.argv:
        idx = sys.argv.index('-c')
        if idx + 1 < len(sys.argv):
            credentials_file = sys.argv[idx + 1]

    # Load credentials
    if path.exists(credentials_file):
        with open(credentials_file, 'rt') as f:
            username, password = f.read().strip().splitlines()
    else:
        raise Exception(f'Credentials file not found: {credentials_file}')

    # Parse ML method (default: knn)
    ml_method = 'knn'
    if '--method' in sys.argv:
        idx = sys.argv.index('--method')
        if idx + 1 < len(sys.argv):
            ml_method = sys.argv[idx + 1]

    # Determine server configuration
    server_config = None
    if '--local' in sys.argv:
        server_config = LocalhostServerConfiguration
        print(f"Starting as {username} on LOCAL server (method: {ml_method})...")
    else:
        print(f"Starting as {username} on OFFICIAL server (method: {ml_method})...")

    # Create the player
    player = Gen1WarriorPlayer(
        username=username,
        password=password,
        training_mode='--train' in sys.argv,
        log_level=log_level,
        server_configuration=server_config,
        ml_method=ml_method,
    )

    # Handle challenge mode
    if '--challenge' in sys.argv:
        idx = sys.argv.index('--challenge')
        if idx + 1 < len(sys.argv):
            challenge_opponent = sys.argv[idx + 1]
            print(f"Will challenge: {challenge_opponent}")
            await player.send_challenges(challenge_opponent, n_challenges=100)
            return

    # Handle ladder mode
    if '--rando' in sys.argv:
        await player.ladder(n_games=100)
    else:
        print("Waiting for challenges...")
        await player.accept_challenges(opponent=None, n_challenges=100)


if __name__ == "__main__":
    asyncio.run(main())
