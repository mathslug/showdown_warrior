#!/usr/bin/env python3
"""
Gen 1 Pokemon Battle Player using poke-env.

This module handles:
- Battle state management via poke-env
- Action selection and ordering
- Training data recording
- Battle lifecycle callbacks

Calculation logic is delegated to battle_thinker.py
"""
import logging
import random
import time
import pandas as pd
from os import path

from poke_env import AccountConfiguration, ShowdownServerConfiguration
from poke_env.player import Player
from poke_env.battle import Battle

from battle_thinker import Gen1BattleThinker


class Gen1WarriorPlayer(Player):
    """Pokemon battle player that uses Gen1BattleThinker for decision making."""

    def __init__(
        self,
        username: str,
        password: str,
        training_mode: bool = False,
        max_concurrent_battles: int = 5,
        log_level: int = logging.INFO,
        server_configuration=None,
        **kwargs
    ):
        super().__init__(
            account_configuration=AccountConfiguration(username, password),
            battle_format="gen1randombattle",
            server_configuration=server_configuration or ShowdownServerConfiguration,
            max_concurrent_battles=max_concurrent_battles,
            log_level=log_level,
            **kwargs
        )
        self.training_mode = training_mode
        self.turn_counter = 0
        self._battle_metrics = self._empty_metrics()
        self._username = username
        self._recent_actions = []  # Track recent actions for switch penalty

        # Initialize the thinker for calculations
        self._thinker = Gen1BattleThinker(username)

        # CSV paths for training data
        self._write_csv = f'./data/battle_records_{username}.csv'

    def _empty_metrics(self) -> dict:
        """Create empty metrics dictionary for a new battle."""
        return {k: [] for k in [
            'turn', 'action', 'self_hp', 'opp_hp', 'outspeed_prob',
            'is_status_move', 'exp_damage_done', 'exp_damage_received',
            'predicted_npw_score'
        ]}

    def choose_move(self, battle: Battle):
        """
        Choose the best move for the current battle state.

        This is called by poke-env when we need to make a decision.
        """
        self.turn_counter = battle.turn

        # Build list of possible actions
        actions = []
        for move in battle.available_moves:
            actions.append(('move', move))
        for pokemon in battle.available_switches:
            actions.append(('switch', pokemon))

        if not actions:
            return self.choose_random_move(battle)

        # Calculate metrics for each action using the thinker
        action_metrics = []
        for action in actions:
            metrics = self._thinker.get_action_metrics(battle, action)
            action_metrics.append(metrics)

        # Apply switch penalty for decision-making
        adjusted_metrics = self._apply_switch_penalty(action_metrics)

        # Log choices
        print(f"\nTurn {self.turn_counter} - CHOICES:")
        for idx, m in enumerate(adjusted_metrics):
            action_type = "SWITCH" if m['is_switch'] else "MOVE"
            print(f"  {idx + 1}: [{action_type}] {m['action_name']}")
            print(f"       score: {m['adjusted_score']:.3f} | dmg_out: {m['exp_damage_done']:.2f} | dmg_in: {m['exp_damage_received']:.2f} | outspeed: {m['outspeed_prob']:.2f}")

        # Select action
        if self.training_mode:
            print("")
            user_inp = int(input('What should we do? '))
            selected_idx = max(0, min(user_inp - 1, len(action_metrics) - 1))
            selected = action_metrics[selected_idx]
        else:
            max_score = max(m['adjusted_score'] for m in adjusted_metrics)
            best = [m for m in adjusted_metrics if m['adjusted_score'] == max_score]
            selected_adjusted = random.choice(best)
            # Find the original (unadjusted) version
            selected = next(m for m in action_metrics if m['action_name'] == selected_adjusted['action_name'])
            time.sleep(1.5)

        # Record the action
        self._record_action(selected)

        # Return the battle order
        action_type, action_obj = selected['battle_order']
        return self.create_order(action_obj)

    def _apply_switch_penalty(self, action_metrics: list) -> list:
        """
        Apply penalty to switch actions based on recent switching frequency.

        This discourages excessive switching which can be a losing strategy.
        Returns metrics with 'adjusted_score' for decision-making, preserving
        original 'predicted_npw_score' for training data.
        """
        # Count recent switches
        recent_switches = sum(1 for action in self._recent_actions[-4:] if action.startswith('switch_'))

        adjusted = []
        for m in action_metrics:
            m_copy = m.copy()
            m_copy['adjusted_score'] = m['predicted_npw_score']

            if recent_switches > 0 and m.get('is_switch', False):
                # Exponential penalty: more recent switches = bigger penalty
                switch_penalty = 0.3 * (2 ** recent_switches)
                m_copy['adjusted_score'] -= switch_penalty

            adjusted.append(m_copy)

        return adjusted

    def _record_action(self, metrics: dict):
        """Record action metrics for training data."""
        self._battle_metrics['turn'].append(self.turn_counter)
        self._battle_metrics['action'].append(metrics['action_name'])
        self._battle_metrics['self_hp'].append(metrics['self_hp'])
        self._battle_metrics['opp_hp'].append(metrics['opp_hp'])
        self._battle_metrics['outspeed_prob'].append(metrics['outspeed_prob'])
        self._battle_metrics['is_status_move'].append(metrics['is_status_move'])
        self._battle_metrics['exp_damage_done'].append(metrics['exp_damage_done'])
        self._battle_metrics['exp_damage_received'].append(metrics['exp_damage_received'])
        self._battle_metrics['predicted_npw_score'].append(metrics['predicted_npw_score'])

        # Track for switch penalty
        action_type = 'switch_' + metrics['action_name'] if metrics.get('is_switch', False) else 'move_' + metrics['action_name']
        self._recent_actions.append(action_type)
        if len(self._recent_actions) > 6:
            self._recent_actions.pop(0)

    def _battle_finished_callback(self, battle: Battle):
        """Called when a battle finishes. Records training data."""
        won = battle.won
        is_tie = won is None
        knight_wins = True if is_tie else won

        result = 'Win' if knight_wins else 'Loss'
        if is_tie:
            result += ' (tie)'
        print(f"\nBattle finished! {result}")

        # Calculate actual NPW scores and save
        if self._battle_metrics['turn']:
            final_turn = max(self._battle_metrics['turn'])
            self._battle_metrics['actual_npw_score'] = [
                (knight_wins / 1.1 ** (final_turn - t)) / (2 if is_tie else 1)
                for t in self._battle_metrics['turn']
            ]
            battle_frame = pd.DataFrame.from_dict(self._battle_metrics)
            battle_frame.to_csv(self._write_csv, index=False)
            print(f"Saved {len(battle_frame)} battle records to {self._write_csv}")

        # Reset for next battle
        self._battle_metrics = self._empty_metrics()
        self.turn_counter = 0
        self._recent_actions = []

        # Call parent's callback
        super()._battle_finished_callback(battle)
