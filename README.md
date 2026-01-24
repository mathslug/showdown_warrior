# showdown_warrior

showdown_warrior is a framework for exploring how different machine learning methods can learn to play Pokemon Showdown using a low-dimensional approximation of battle state.

## Motivation

Pokemon battles have complex, high-dimensional state spaces: six Pokemon per side, four moves each, stats, items, abilities, weather, entry hazards, and more. Traditional deep learning approaches would encode this full state and learn end-to-end.

This project takes a different approach: we hand-craft a small set of features that capture the essence of a battle decision, then compare how various ML methods learn from this compressed representation. The current feature set includes:

- `self_hp` / `opp_hp` - HP fractions
- `outspeed_prob` - probability of moving first
- `is_status_move` - status effect probability
- `exp_damage_done` / `exp_damage_received` - expected damage exchange

This low-dimensional approach lets us:
- Train quickly with limited data
- Compare classical ML methods (KNN, gradient boosting, etc.) directly
- Understand what the model is learning

In the future, this could be extended to methods that work in high dimensions, taking a more traditional deep learning approach with raw state encoding.

## Available ML Methods

- `knn` - K-Nearest Neighbors (default)
- `gb` - Gradient Boosting

Select via the `--method` flag or when running continuous battles.

## Setup

1. Clone this repository and cd into it

2. Save Showdown credentials in `./data/login.txt`:
   ```
   username
   password
   ```

3. Install dependencies:
   ```bash
   poetry install
   # or: uv sync
   ```

4. Run the bot:
   ```bash
   poetry run python start_warrior.py
   # or: uv run python start_warrior.py
   ```

## Continuous Training

For self-play training that accumulates data across battles:

```bash
# Both bots use KNN (default)
./continuous_battles.sh

# Bot 1 uses gradient boosting, bot 2 uses KNN
./continuous_battles.sh gb knn
```

This runs battles in tmux, combining training data between rounds.

## Project Structure

- `start_warrior.py` - Entry point
- `warrior_player.py` - Battle lifecycle and action selection
- `thinkers/` - ML method implementations
  - `feature_engineering.py` - Shared feature calculations
  - `knn_thinker.py` - KNN implementation
  - `gb_thinker.py` - Gradient boosting implementation
- `continuous_battles.sh` - Self-play training script

## TODO

The following Gen 1 mechanics are not yet modeled in feature engineering:

- [ ] Multi-hit moves (Double Kick, Pin Missile, etc.)
- [ ] Trapping moves (Wrap, Bind, Fire Spin)
- [ ] Explosion / Self-Destruct (user fainting cost)
- [ ] Critical hit modeling (speed-based crit rates in Gen 1)

## Ethics

This bot is intended for testing and research. Do not use it to challenge random players on the official Pokemon Showdown server. For large-scale training or continuous testing, host your own Showdown instance.

## License

MIT License
