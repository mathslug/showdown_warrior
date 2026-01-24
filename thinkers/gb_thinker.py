#!/usr/bin/env python3
"""Gradient Boosting based thinker for Gen 1 Pokemon battle decisions."""
import pandas as pd
from os import path
from sklearn.ensemble import GradientBoostingRegressor
from poke_env.battle import Battle

from .feature_engineering import compute_features, FEATURE_COLS


class GradientBoostThinker:
    """Gradient Boosting based battle thinker."""

    method_name = 'gb'

    def __init__(self, username: str):
        self._username = username
        self._csv_path = './data/battle_records_combined.csv'
        self._load_training_data()

    def _load_training_data(self):
        """Load training data and fit Gradient Boosting model."""
        if path.exists(self._csv_path):
            self._training_data = pd.read_csv(self._csv_path, index_col=False)
            self._model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=4,
                learning_rate=0.1,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42
            ).fit(
                self._training_data[FEATURE_COLS],
                self._training_data.actual_npw_score
            )
            self._predict = lambda df: self._model.predict(df)[0]
            print(f"[GB] Loaded {len(self._training_data)} training records from {self._csv_path}")
        else:
            self._training_data = pd.DataFrame()
            self._predict = lambda df: 0
            print(f"[GB] No training data found at {self._csv_path}, starting fresh")

    def get_action_metrics(self, battle: Battle, action: tuple) -> dict:
        """Calculate all metrics for a given action."""
        m = compute_features(battle, action)
        metrics_df = pd.DataFrame({k: [m[k]] for k in FEATURE_COLS})
        m['predicted_npw_score'] = self._predict(metrics_df)
        return m
