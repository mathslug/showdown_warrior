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

* save showdown credentials in `./data/login.txt` as:

```
username
password
```

* recommended: activate a virtualenv. I use poetry.

* `poetry install`

* `poetry run python start_warrior.py`

* you're done, go battle it on showdown

* control-c to stop it

## Customization

Core logic lives in thinker.py. You can modify or replace it to try different reinforcement learning methods, state representations or engineered features.

## Background

A full write-up of the design and intent is available here:
👉 https://mathslug.com/posts/showdown/

## Future Work

Add ability to support more generations of Pokémon.

## License

MIT License
