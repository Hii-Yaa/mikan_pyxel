"""Fruit data structures and management."""
import random
from typing import Optional
from game.config import game_config


class Fruit:
    """Represents a single fruit in the game."""

    def __init__(self, stage: int, x: float, y: float, fresh: Optional[float] = None):
        """
        Initialize a fruit.

        Args:
            stage: Fruit stage (0-5: ume, kaki, momo, budou, dekopon, mikan)
            x: X position
            y: Y position
            fresh: Freshness value (auto-generated if None)
        """
        self.stage = stage
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

        # Get fruit properties from config
        fruit_data = game_config.get("fruits")[stage]
        self.name = fruit_data["name"]
        self.display_name = fruit_data["display_name"]
        self.radius = fruit_data["radius"]
        self.color = fruit_data["color"]

        # Freshness
        if fresh is None:
            self.fresh = self._generate_fresh()
        else:
            self.fresh = fresh

        # State
        self.dropped = False  # True when dropped into play area
        self.merge_cooldown = 0.0  # Prevents immediate re-merging

    def _generate_fresh(self) -> float:
        """Generate random freshness value based on config."""
        fresh_max = game_config.get("freshness", "fresh_max", default=100)
        spawn_min = game_config.get("freshness", "spawn_min", default=50)
        spawn_max = game_config.get("freshness", "spawn_max", default=100)
        distribution = game_config.get("freshness", "spawn_distribution", default="triangular")

        if distribution == "uniform":
            return random.uniform(spawn_min, spawn_max)
        else:  # triangular
            # Triangular with mode at max (bias toward high freshness)
            return random.triangular(spawn_min, spawn_max, spawn_max)

    def update_decay(self, dt: float) -> None:
        """Update freshness decay over time."""
        if not self.dropped:
            return

        decay_base = game_config.get("freshness", "decay_base", default=2.0)
        decay_mult = game_config.get("freshness", "decay_stage_mult", default=1.2)

        # Higher stages decay faster
        decay_rate = decay_base * (decay_mult ** self.stage)
        self.fresh = max(0, self.fresh - decay_rate * dt)

        # Update merge cooldown
        if self.merge_cooldown > 0:
            self.merge_cooldown -= dt

    def get_freshness_level(self) -> str:
        """Get freshness level for visual effects."""
        fresh_max = game_config.get("freshness", "fresh_max", default=100)
        ratio = self.fresh / fresh_max

        if ratio > 0.7:
            return "high"
        elif ratio > 0.4:
            return "medium"
        elif ratio > 0.15:
            return "low"
        else:
            return "rotten"

    def is_mikan(self) -> bool:
        """Check if this is a mikan (final stage)."""
        return self.stage == 5

    def can_merge(self) -> bool:
        """Check if fruit can participate in merging."""
        return self.dropped and self.merge_cooldown <= 0


class FruitFactory:
    """Factory for creating fruits."""

    @staticmethod
    def create_spawn_fruit(x: float = 120) -> Fruit:
        """
        Create a new fruit for spawning.

        Initial fruits are limited to first 3 stages.
        """
        stage = random.randint(0, 2)  # ume, kaki, or momo
        return Fruit(stage, x, 50)

    @staticmethod
    def create_merged_fruit(stage: int, x: float, y: float,
                           fresh_a: float, fresh_b: float) -> Fruit:
        """
        Create a fruit from merging two others.

        Args:
            stage: New fruit stage
            x, y: Position
            fresh_a, fresh_b: Freshness values of parent fruits
        """
        merge_bonus = game_config.get("freshness", "merge_bonus", default=20)
        fresh_cap = game_config.get("freshness", "fresh_cap", default=100)

        # Combine freshness with bonus
        new_fresh = min(fresh_cap, fresh_a + fresh_b + merge_bonus)

        fruit = Fruit(stage, x, y, new_fresh)
        fruit.dropped = True

        # Set cooldown to prevent immediate re-merge
        cooldown = game_config.get("physics", "merge_cooldown", default=0.5)
        fruit.merge_cooldown = cooldown

        return fruit
