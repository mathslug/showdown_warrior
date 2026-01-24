"""Base interface for ML thinkers."""
from typing import Protocol, Any


class BaseThinker(Protocol):
    """Interface all thinkers must implement."""

    method_name: str  # e.g., 'knn', 'gb' - used for CSV naming

    def get_action_metrics(self, battle: Any, action: tuple) -> dict:
        """
        Calculate metrics for a potential action.

        Args:
            battle: The current battle state
            action: Tuple of (action_type, action_obj) where action_type is 'move' or 'switch'

        Returns:
            dict with at minimum:
            - predicted_npw_score: float - ML model prediction for this action
            - action_name: str - Name of the action (move id or pokemon species)
            - is_switch: bool - Whether this action is a switch
            - battle_order: tuple of (action_type, action_obj) for creating the order

            May include additional method-specific metrics.
        """
        ...
