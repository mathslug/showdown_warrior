#!/usr/bin/env python3
"""KNN-based thinker for Gen 1 Pokemon battle decisions."""
import math
import pandas as pd
from os import path
from sklearn.neighbors import KNeighborsRegressor
from poke_env.battle import Battle

from .feature_engineering import compute_features, FEATURE_COLS


class KNNThinker:
    """KNN-based battle thinker."""

    method_name = 'knn'

    def __init__(self, username: str):
        self._username = username
        self._csv_path = './data/battle_records_combined.csv'
        self._load_training_data()

    def _load_training_data(self):
        """Load KNN training data from CSV if available."""
        if path.exists(self._csv_path):
            self._training_data = pd.read_csv(self._csv_path, index_col=False)
            n_neighbors = max(1, math.floor(math.sqrt(self._training_data.shape[0])))
            self._model = KNeighborsRegressor(n_neighbors=n_neighbors).fit(
                self._training_data[FEATURE_COLS],
                self._training_data.actual_npw_score
            )
            self._predict = lambda df: self._model.predict(df)[0]
            print(f"[KNN] Loaded {len(self._training_data)} training records from {self._csv_path}")
        else:
            self._training_data = pd.DataFrame()
            self._predict = lambda df: 0
            print(f"[KNN] No training data found at {self._csv_path}, starting fresh")

    def get_action_metrics(self, battle: Battle, action: tuple) -> dict:
        """Calculate all metrics for a given action."""
        m = compute_features(battle, action)
        metrics_df = pd.DataFrame({k: [m[k]] for k in FEATURE_COLS})
        m['predicted_npw_score'] = self._predict(metrics_df)
        return m
