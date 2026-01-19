"""Merge detection and execution logic."""
from typing import List, Optional, Tuple
from game.fruit import Fruit, FruitFactory
from game.physics import PhysicsEngine


class MergeManager:
    """Manages fruit merging logic."""

    def __init__(self, physics: PhysicsEngine):
        """
        Initialize merge manager.

        Args:
            physics: Physics engine for collision detection
        """
        self.physics = physics

    def check_and_merge(self, fruits: List[Fruit]) -> List[Tuple[Fruit, Fruit, Fruit]]:
        """
        Check for mergeable fruits and create merged fruits.

        Args:
            fruits: List of fruits to check

        Returns:
            List of (fruit_a, fruit_b, merged_fruit) tuples
        """
        merges = []

        i = 0
        while i < len(fruits):
            fruit_a = fruits[i]

            if not fruit_a.can_merge():
                i += 1
                continue

            # Look for matching fruit to merge
            j = i + 1
            merged = False

            while j < len(fruits):
                fruit_b = fruits[j]

                if not fruit_b.can_merge():
                    j += 1
                    continue

                # Check if same stage and colliding
                if fruit_a.stage == fruit_b.stage:
                    if self.physics.check_collision(fruit_a, fruit_b):
                        # Create merged fruit
                        merged_fruit = self._merge_fruits(fruit_a, fruit_b)
                        merges.append((fruit_a, fruit_b, merged_fruit))
                        merged = True
                        break

                j += 1

            if merged:
                # Don't increment i, check same position again
                continue

            i += 1

        return merges

    def _merge_fruits(self, fruit_a: Fruit, fruit_b: Fruit) -> Fruit:
        """
        Merge two fruits into a higher stage fruit.

        Args:
            fruit_a: First fruit
            fruit_b: Second fruit

        Returns:
            New merged fruit
        """
        # Calculate merge position (midpoint)
        merge_x = (fruit_a.x + fruit_b.x) / 2
        merge_y = (fruit_a.y + fruit_b.y) / 2

        # Next stage
        new_stage = fruit_a.stage + 1

        # Create merged fruit with combined freshness
        merged = FruitFactory.create_merged_fruit(
            new_stage,
            merge_x,
            merge_y,
            fruit_a.fresh,
            fruit_b.fresh
        )

        # Inherit average velocity
        merged.vx = (fruit_a.vx + fruit_b.vx) / 2
        merged.vy = (fruit_a.vy + fruit_b.vy) / 2

        return merged

    def apply_merges(self, fruits: List[Fruit],
                     merges: List[Tuple[Fruit, Fruit, Fruit]]) -> List[Fruit]:
        """
        Apply merge operations to fruit list.

        Args:
            fruits: Current fruit list
            merges: List of merge operations

        Returns:
            List of newly created mikan (for delivery)
        """
        if not merges:
            return []

        # Collect fruits to remove
        to_remove = set()
        for fruit_a, fruit_b, _ in merges:
            to_remove.add(fruit_a)
            to_remove.add(fruit_b)

        # Remove merged fruits
        fruits[:] = [f for f in fruits if f not in to_remove]

        # Add new fruits and collect mikan
        delivered_mikan = []
        for _, _, merged in merges:
            if merged.is_mikan():
                # Mikan are delivered immediately (don't add to play area)
                delivered_mikan.append(merged)
            else:
                fruits.append(merged)

        return delivered_mikan
