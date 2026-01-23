# showdown_warrior

showdown_warrior learns how to play Pokémon Showdown. It's a modular tool for experimenting with machine learning and decision-making strategies in Pokémon Showdown.

It provides a clean interface to the Showdown API, handles authentication and connection recovery, and allows you to rapidly prototype and test AI agents that learn as they battle.

## Overview

This project isn’t a single “best” algorithm—it’s a framework for exploring how different ML and heuristic methods perform in Pokémon Showdown battles.
You can customize how the bot perceives game state, what data it tracks, and how it decides the next move. You can have the bot learn by itself, or have the bot watch you and learn your playstyle.

**Goals**

- Modular architecture: swap out decision modules or data trackers easily.

- Self-play and online learning: agents can learn from matches against themselves or human players.

- Robust integration: automatically reconnects and syncs with the Showdown API after dropped connections.

- Safe experimentation: intended for testing and research, not online farming or spam battles. Do not use this bot to challenge random players on the official Pokémon Showdown server. For large-scale training or continuous testing, please host your own Showdown instance.

## Setup

* git clone this repository and cd into it

* save showdown credentials in a text file (default: `./data/login.txt`) as:

```
username
password
```

* install uv if you don't have it

* `uv sync`

* `uv run python start_warrior.py`

* go battle it

* control-c to stop it

## Usage

Basic usage:
```bash
uv run python start_warrior.py
```

With custom credentials file:
```bash
uv run python start_warrior.py --credentials path/to/mycreds.txt
# or
uv run python start_warrior.py -c path/to/mycreds.txt
```

Additional options:
- `--debug` - Enable debug logging
- `--train` - Enable training mode (prompts for manual action selection)
- `--rando` - Play 100 ladder games instead of waiting for challenges
- `--local` - Connect to a local Pokémon Showdown server (localhost:8000)
- `--challenge <username>` - Send challenges to a specific user instead of accepting challenges

## Local Self-Play Battles

To run continuous training battles between two bots on a local Pokémon Showdown server:

1. Clone the Pokémon Showdown server in the parent directory:
   ```bash
   cd ..
   git clone https://github.com/smogon/pokemon-showdown.git
   cd pokemon-showdown
   npm install
   cd ../showdown_warrior
   ```

2. Create credentials for two bots in `data/login2.txt` (if you don't have it already):
   ```
   bot2username
   bot2password
   ```

3. Run continuous training battles:
   ```bash
   ./continuous_battles.sh
   ```

This script will:
- Start a local Pokémon Showdown server
- Run battles continuously in a loop
- After each battle:
  - Combine training data from both bots
  - Restart the bots so they learn from all previous battles
  - Start the next battle automatically

The bots will get progressively better as they accumulate training data!

**Monitoring:**
- Watch battles live: `tmux attach -t showdown_battle`
  - `<prefix> 0` to switch to server window
  - `<prefix> 1` to switch to bots window
  - `<prefix> d` to detach (keeps it running)
- View training data: `cat data/battle_records_combined.csv | wc -l`
- Stop training: `Ctrl+C` in the terminal running the script

## Customization

Core logic lives in warrior_player.py. You can modify or replace it to try different reinforcement learning methods, state representations or engineered features.

## Background

A full write-up of the design and intent is available here:
👉 https://mathslug.com/posts/showdown/

## Future Work

Add ability to support more generations of Pokémon.

## License

MIT License
