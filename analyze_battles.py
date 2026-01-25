#!/usr/bin/env python3
"""Analyze battle records and generate cumulative wins graph."""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def analyze_battles():
    """Load battle data and create cumulative wins visualization."""
    # Load the data
    df = pd.read_csv('data/battle_records_combined.csv')

    # Filter to only wins (actual_npw_score == 1.0) and keep the original index
    wins = df[df['actual_npw_score'] == 1.0].copy()

    # Each battle has exactly one winner, so sequential win count = battle number
    wins['battle_number'] = range(1, len(wins) + 1)

    # Calculate cumulative wins for each method
    wins['cumulative_wins'] = wins.groupby('ml_method').cumcount() + 1

    knn_wins = wins[wins['ml_method'] == 'knn']
    gb_wins = wins[wins['ml_method'] == 'gb']

    # Create the plot
    plt.figure(figsize=(12, 6))

    plt.plot(knn_wins['battle_number'], knn_wins['cumulative_wins'],
                label='KNN', linewidth=2, marker='o', markersize=3)

    plt.plot(gb_wins['battle_number'], gb_wins['cumulative_wins'],
                label='Gradient Boosting', linewidth=2, marker='s', markersize=3)

    plt.xlabel('Number of Battles', fontsize=12)
    plt.ylabel('Cumulative Wins', fontsize=12)
    plt.title('Cumulative Wins Over Time: KNN vs Gradient Boosting', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Save the plot
    output_path = Path('./cumulative_wins.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Graph saved to {output_path}")

    # Print summary statistics
    print(f"\nBattle Summary:")
    print(f"Total wins analyzed: {len(wins)}")
    if len(knn_wins) > 0:
        print(f"KNN: {len(knn_wins)} wins")
    if len(gb_wins) > 0:
        print(f"GB: {len(gb_wins)} wins")


if __name__ == '__main__':
    analyze_battles()
