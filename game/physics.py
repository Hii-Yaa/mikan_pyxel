"""Custom 2D circle physics engine."""
import math
from typing import List
from game.fruit import Fruit
from game.config import game_config


class PhysicsEngine:
    """Handles physics simulation for circular fruits."""

    def __init__(self, width: int, height: int):
        """
        Initialize physics engine.

        Args:
            width: Play area width
            height: Play area height
        """
        self.width = width
        self.height = height

    def update(self, fruits: List[Fruit], dt: float) -> None:
        """
        Update physics for all fruits.

        Args:
            fruits: List of fruits to update
            dt: Delta time in seconds
        """
        gravity = game_config.get("physics", "gravity", default=300.0)
        friction = game_config.get("physics", "friction", default=0.98)

        for fruit in fruits:
            if not fruit.dropped:
                continue

            # Apply gravity
            fruit.vy += gravity * dt

            # Apply friction
            fruit.vx *= friction
            fruit.vy *= friction

            # Update position
            fruit.x += fruit.vx * dt
            fruit.y += fruit.vy * dt

        # Resolve collisions
        self._resolve_wall_collisions(fruits)
        self._resolve_fruit_collisions(fruits)

    def _resolve_wall_collisions(self, fruits: List[Fruit]) -> None:
        """Resolve collisions with walls and floor."""
        bounce = game_config.get("physics", "bounce", default=0.3)

        for fruit in fruits:
            if not fruit.dropped:
                continue

            # Left wall
            if fruit.x - fruit.radius < 0:
                fruit.x = fruit.radius
                fruit.vx = abs(fruit.vx) * bounce

            # Right wall
            if fruit.x + fruit.radius > self.width:
                fruit.x = self.width - fruit.radius
                fruit.vx = -abs(fruit.vx) * bounce

            # Floor
            if fruit.y + fruit.radius > self.height:
                fruit.y = self.height - fruit.radius
                fruit.vy = -abs(fruit.vy) * bounce

                # Stop if moving slowly
                if abs(fruit.vy) < 10:
                    fruit.vy = 0

    def _resolve_fruit_collisions(self, fruits: List[Fruit]) -> None:
        """Resolve collisions between fruits."""
        for i in range(len(fruits)):
            for j in range(i + 1, len(fruits)):
                fruit_a = fruits[i]
                fruit_b = fruits[j]

                if not fruit_a.dropped or not fruit_b.dropped:
                    continue

                # Check collision
                dx = fruit_b.x - fruit_a.x
                dy = fruit_b.y - fruit_a.y
                dist = math.sqrt(dx * dx + dy * dy)
                min_dist = fruit_a.radius + fruit_b.radius

                if dist < min_dist and dist > 0:
                    # Separate fruits
                    overlap = min_dist - dist
                    nx = dx / dist
                    ny = dy / dist

                    # Move apart proportionally
                    fruit_a.x -= nx * overlap * 0.5
                    fruit_a.y -= ny * overlap * 0.5
                    fruit_b.x += nx * overlap * 0.5
                    fruit_b.y += ny * overlap * 0.5

                    # Bounce (elastic collision)
                    relative_vx = fruit_b.vx - fruit_a.vx
                    relative_vy = fruit_b.vy - fruit_a.vy
                    dot_product = relative_vx * nx + relative_vy * ny

                    if dot_product < 0:  # Moving towards each other
                        bounce = game_config.get("physics", "bounce", default=0.3)

                        fruit_a.vx += nx * dot_product * bounce
                        fruit_a.vy += ny * dot_product * bounce
                        fruit_b.vx -= nx * dot_product * bounce
                        fruit_b.vy -= ny * dot_product * bounce

    def check_collision(self, fruit_a: Fruit, fruit_b: Fruit) -> bool:
        """
        Check if two fruits are colliding.

        Args:
            fruit_a: First fruit
            fruit_b: Second fruit

        Returns:
            True if colliding
        """
        dx = fruit_b.x - fruit_a.x
        dy = fruit_b.y - fruit_a.y
        dist = math.sqrt(dx * dx + dy * dy)
        min_dist = fruit_a.radius + fruit_b.radius

        return dist < min_dist
