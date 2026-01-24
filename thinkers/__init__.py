"""Thinker factory for modular ML methods."""
from .knn_thinker import KNNThinker
from .gb_thinker import GradientBoostThinker

THINKERS = {
    'knn': KNNThinker,
    'gb': GradientBoostThinker,
}


def create_thinker(username: str, method: str = 'knn'):
    """
    Create a thinker instance for the given ML method.

    Args:
        username: The player's username
        method: The ML method to use ('knn', 'gb')

    Returns:
        A thinker instance implementing the BaseThinker protocol

    Raises:
        ValueError: If the method is not recognized
    """
    if method not in THINKERS:
        raise ValueError(f"Unknown method '{method}'. Available: {list(THINKERS.keys())}")
    return THINKERS[method](username)
