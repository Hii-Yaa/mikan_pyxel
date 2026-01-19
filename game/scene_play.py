"""Main play scene with game logic."""
import pyxel
import time
from typing import List
from game.fruit import Fruit, FruitFactory
from game.physics import PhysicsEngine
from game.merge import MergeManager
from game.scoring import ScoreTracker
from game.ui_beta import BetaPanel, HUD
from game.config import game_config


class PlayScene:
    """Main gameplay scene."""

    # Play area dimensions
    PLAY_WIDTH = 240
    PLAY_HEIGHT = 200
    PLAY_X = 0
    PLAY_Y = 40

    def __init__(self, app):
        """
        Initialize play scene.

        Args:
            app: Main application instance
        """
        self.app = app

        # Game state
        self.fruits: List[Fruit] = []
        self.next_fruit: Fruit = None
        self.drop_cooldown = 0.0
        self.paused = False
        self.game_over = False
        self.game_over_reason = ""

        # Game systems
        self.physics = PhysicsEngine(self.PLAY_WIDTH, self.PLAY_HEIGHT)
        self.merge_manager = MergeManager(self.physics)
        self.score_tracker = ScoreTracker()
        self.beta_panel = BetaPanel()

        # Game over detection
        self.above_line_time = 0.0
        self.danger_line_y = 0

        # Initialize
        self.reset()

    def reset(self) -> None:
        """Reset game to initial state."""
        self.fruits.clear()
        self.next_fruit = FruitFactory.create_spawn_fruit(self.PLAY_WIDTH // 2)
        self.drop_cooldown = 0.0
        self.paused = False
        self.game_over = False
        self.game_over_reason = ""
        self.score_tracker.reset()
        self.above_line_time = 0.0

        # Calculate danger line
        line_y_ratio = game_config.get("game_over", "line_y", default=0.2)
        self.danger_line_y = int(self.PLAY_HEIGHT * line_y_ratio)

    def update(self) -> None:
        """Update play scene."""
        # Beta panel controls
        if pyxel.btnp(pyxel.KEY_F1):
            self.beta_panel.toggle()

        if pyxel.btnp(pyxel.KEY_F5):
            game_config.save()

        if pyxel.btnp(pyxel.KEY_F9):
            game_config.reset_to_defaults()

        # Update beta panel
        if self.beta_panel.visible:
            self.beta_panel.update()
            return  # Don't update game when panel is open

        # Pause toggle
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.paused = not self.paused

        if self.paused or self.game_over:
            # Check for ship out during pause or game over
            if pyxel.btnp(pyxel.KEY_S):
                self._end_game("SHIPPED OUT")
            return

        # Ship out at any time
        if pyxel.btnp(pyxel.KEY_S):
            self._end_game("SHIPPED OUT")
            return

        # Update drop cooldown
        dt = 1.0 / 30.0  # Assume 30 FPS
        if self.drop_cooldown > 0:
            self.drop_cooldown -= dt

        # Update next fruit position
        if self.next_fruit and not self.next_fruit.dropped:
            # Mouse control
            mouse_x = pyxel.mouse_x
            self.next_fruit.x = max(self.next_fruit.radius,
                                   min(self.PLAY_WIDTH - self.next_fruit.radius, mouse_x))

            # Drop on click
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.drop_cooldown <= 0:
                self._drop_fruit()

        # Update physics
        self.physics.update(self.fruits, dt)

        # Update freshness decay
        for fruit in self.fruits:
            fruit.update_decay(dt)

        # Check and apply merges
        merges = self.merge_manager.check_and_merge(self.fruits)
        delivered_mikan = self.merge_manager.apply_merges(self.fruits, merges)

        # Deliver mikan
        for mikan in delivered_mikan:
            self.score_tracker.deliver_mikan(mikan.fresh)

        # Check game over condition
        self._check_game_over(dt)

    def _drop_fruit(self) -> None:
        """Drop the current fruit."""
        if not self.next_fruit:
            return

        # Mark as dropped
        self.next_fruit.dropped = True
        self.next_fruit.y = self.PLAY_Y  # Start from top of play area
        self.fruits.append(self.next_fruit)

        # Create next fruit
        self.next_fruit = FruitFactory.create_spawn_fruit(self.PLAY_WIDTH // 2)
        self.drop_cooldown = 0.5  # Half second cooldown

    def _check_game_over(self, dt: float) -> None:
        """
        Check if game over condition is met.

        Args:
            dt: Delta time
        """
        # Check if any fruit is above danger line
        grace_ms = game_config.get("game_over", "grace_ms", default=3000)
        grace_seconds = grace_ms / 1000.0

        any_above = False
        for fruit in self.fruits:
            if fruit.y - fruit.radius < self.danger_line_y:
                any_above = True
                break

        if any_above:
            self.above_line_time += dt
            if self.above_line_time >= grace_seconds:
                self._end_game("JAMMED!")
        else:
            self.above_line_time = 0.0

    def _end_game(self, reason: str) -> None:
        """
        End the game and show results.

        Args:
            reason: Reason for game over
        """
        self.game_over = True
        self.game_over_reason = reason

        # Switch to result scene
        result_scene = self.app.scenes["result"]
        result_scene.set_result(self.score_tracker, reason)
        self.app.change_scene("result")

    def draw(self) -> None:
        """Draw play scene."""
        pyxel.cls(0)

        # Draw play area background
        pyxel.rect(self.PLAY_X, self.PLAY_Y,
                  self.PLAY_WIDTH, self.PLAY_HEIGHT, 1)

        # Draw danger line
        danger_y = self.PLAY_Y + self.danger_line_y
        line_color = 8 if self.above_line_time > 0 else 2
        pyxel.line(self.PLAY_X, danger_y,
                  self.PLAY_X + self.PLAY_WIDTH, danger_y, line_color)

        # Draw grace timer if in danger
        if self.above_line_time > 0:
            grace_ms = game_config.get("game_over", "grace_ms", default=3000)
            remaining = grace_ms / 1000.0 - self.above_line_time
            pyxel.text(5, danger_y - 8, f"DANGER: {remaining:.1f}s", 8)

        # Draw fruits
        fresh_max = game_config.get("freshness", "fresh_max", default=100)
        for fruit in self.fruits:
            # Draw fruit circle
            screen_x = self.PLAY_X + fruit.x
            screen_y = self.PLAY_Y + fruit.y
            pyxel.circ(screen_x, screen_y, fruit.radius, fruit.color)
            pyxel.circb(screen_x, screen_y, fruit.radius, 7)

            # Draw freshness indicator (no numeric value)
            HUD.draw_freshness_indicator(screen_x, screen_y,
                                        fruit.fresh, fresh_max, False)

        # Draw next fruit (not dropped yet)
        if self.next_fruit and not self.next_fruit.dropped:
            screen_x = self.PLAY_X + self.next_fruit.x
            screen_y = 20

            pyxel.circ(screen_x, screen_y, self.next_fruit.radius, self.next_fruit.color)
            pyxel.circb(screen_x, screen_y, self.next_fruit.radius, 7)

            # Show freshness VALUE before dropping
            HUD.draw_freshness_indicator(screen_x, screen_y,
                                        self.next_fruit.fresh, fresh_max, True)

            # Show fruit name
            name_x = screen_x - len(self.next_fruit.display_name) * 2
            pyxel.text(name_x, screen_y - 25, self.next_fruit.display_name, 7)

        # Draw UI
        HUD.draw_score_panel(self.PLAY_WIDTH + 5, 5, self.score_tracker)

        # Draw controls hint
        pyxel.text(5, 5, "ESC:Pause S:Ship F1:Beta", 6)

        # Draw pause overlay
        if self.paused:
            pyxel.rect(self.PLAY_X + 50, self.PLAY_Y + 80, 140, 40, 1)
            pyxel.rectb(self.PLAY_X + 50, self.PLAY_Y + 80, 140, 40, 7)
            pyxel.text(self.PLAY_X + 90, self.PLAY_Y + 90, "PAUSED", 11)
            pyxel.text(self.PLAY_X + 60, self.PLAY_Y + 100, "ESC:Resume S:Ship", 7)

        # Draw beta panel (if visible)
        self.beta_panel.draw(pyxel.width, pyxel.height)
