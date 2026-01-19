"""Scoring system with freshness and rot mechanics."""
from typing import List
from game.config import game_config


class ScoreTracker:
    """Tracks delivered mikan and calculates score."""

    def __init__(self):
        """Initialize score tracker."""
        self.delivered_count = 0  # Total mikan delivered
        self.rotten_count = 0  # Rotten mikan count
        self.fresh_sum = 0.0  # Sum of all fresh values at delivery
        self.delivered_fresh_values: List[float] = []  # History

    def deliver_mikan(self, fresh: float) -> None:
        """
        Deliver a mikan and update tracking.

        Args:
            fresh: Freshness value at delivery
        """
        self.delivered_count += 1
        self.fresh_sum += fresh
        self.delivered_fresh_values.append(fresh)

        # Check if rotten
        rotten_threshold = game_config.get("rot", "rotten_threshold", default=30)
        if fresh <= rotten_threshold:
            self.rotten_count += 1

    def get_effective_fresh(self) -> float:
        """
        Calculate effective freshness after rot damage.

        Formula: effective_fresh = fresh_sum × (1 - rot_rate)^rotten_count
        """
        if self.rotten_count == 0:
            return self.fresh_sum

        rot_rate = game_config.get("rot", "rot_rate", default=0.08)
        multiplier = (1 - rot_rate) ** self.rotten_count

        return self.fresh_sum * multiplier

    def get_score(self) -> int:
        """
        Calculate total score.

        Formula: score = effective_fresh × fresh_to_score + delivered_count × count_bonus
        """
        effective_fresh = self.get_effective_fresh()

        fresh_to_score = game_config.get("score", "fresh_to_score", default=1.0)
        count_bonus = game_config.get("score", "count_bonus", default=40)

        score = effective_fresh * fresh_to_score + self.delivered_count * count_bonus
        return int(score)

    def get_rot_damage_percent(self) -> float:
        """Get percentage of fresh value lost to rot."""
        if self.fresh_sum == 0:
            return 0.0

        effective = self.get_effective_fresh()
        damage = self.fresh_sum - effective
        return (damage / self.fresh_sum) * 100

    def reset(self) -> None:
        """Reset all tracking."""
        self.delivered_count = 0
        self.rotten_count = 0
        self.fresh_sum = 0.0
        self.delivered_fresh_values.clear()
