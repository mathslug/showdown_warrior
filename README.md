# showdown_warrior

A framework for exploring what classical ML methods can learn about Pokemon battles from a deliberately simplified feature set.

## Motivation

Pokemon battles have complex state spaces. Deep learning approaches typically encode full state and learn end-to-end. This project goes a difderent way: hand-craft a minimal feature set, directly apply classical ML, and see what strategy emerges.

**Features** (6 dimensions):
- `self_hp` / `opp_hp` -- HP fractions
- `outspeed_prob` -- probability of moving first
- `is_status_move` -- whether the move applies status
- `exp_damage_done` / `exp_damage_received` -- expected damage exchange

**Target**: Each move is labeled with a discounted win score based on turns remaining. This sidesteps credit assignment with the simple heuristic that later moves in winning games score higher.

**Hypothesis**: Even with this compressed representation, models should learn basic tactics: take KOs when available, avoid obvious KO risk, prefer favorable damage trades. Gradient boosting should pick this up faster than KNN given its ability to learn non-linear decision boundaries.

## Results

KNN vs Gradient Boosting in self-play, both training on the same accumulated data:

![Cumulative Wins Over Time](./cumulative_wins.png)

GB pulls ahead, suggesting it extracts more from the limited feature set. Future work: analyze *what* tactics each method learns, not just win rate.

## ML Methods

- `knn` — K-Nearest Neighbors (default)
- `gb` — Gradient Boosting

Select with `--method`.

## Setup

1. Save credentials in `./data/login.txt`:
   ```
   username
   password
   ```

2. Install and run:
   ```bash
   uv sync
   uv run python start_warrior.py
   ```

## Self-Play Training

Continuous battles with data accumulation:

```bash
./continuous_battles.sh           # both use KNN
./continuous_battles.sh gb knn    # GB vs KNN
```

Requires tmux and a local pokemon-showdown server in `../pokemon-showdown`.

## Project Structure

- `start_warrior.py` -- entry point
- `warrior_player.py` -- battle logic and action selection
- `thinkers/` -- ML implementations
- `continuous_battles.sh` -- self-play loop

## Future Work

- Analyze learned tactics beyond win rate
- Gen 1 critical hit modeling (speed-based crit rates)
- Skip auth for local battles
- Compare against deep RL with raw state encoding

## Ethics

For research only. Don't use this to battle random players on official Showdown servers. Host your own instance for extensive training.

## License

MIT
