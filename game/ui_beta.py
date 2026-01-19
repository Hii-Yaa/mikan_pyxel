"""Beta adjustment UI panel for parameter tuning."""
import pyxel
from game.config import game_config


class BetaPanel:
    """In-game parameter adjustment panel for beta testing."""

    def __init__(self):
        """Initialize beta panel."""
        self.visible = False
        self.scroll = 0
        self.selected_param = None

        # Parameter definitions (category, key, label, min, max, step)
        self.params = [
            ("freshness", "fresh_max", "Fresh Max", 50, 200, 10),
            ("freshness", "spawn_min", "Spawn Min", 0, 100, 5),
            ("freshness", "spawn_max", "Spawn Max", 50, 150, 5),
            ("freshness", "decay_base", "Decay Base", 0.5, 10.0, 0.5),
            ("freshness", "decay_stage_mult", "Decay Stage x", 1.0, 2.0, 0.1),
            ("freshness", "merge_bonus", "Merge Bonus", 0, 50, 5),
            ("freshness", "fresh_cap", "Fresh Cap", 50, 200, 10),
            ("rot", "rotten_threshold", "Rotten Thresh", 0, 100, 5),
            ("rot", "rot_rate", "Rot Rate", 0.0, 0.3, 0.01),
            ("score", "fresh_to_score", "Fresh->Score", 0.1, 5.0, 0.1),
            ("score", "count_bonus", "Count Bonus", 0, 100, 10),
            ("game_over", "line_y", "Line Y", 0.1, 0.5, 0.05),
            ("game_over", "grace_ms", "Grace (ms)", 1000, 10000, 500),
        ]

    def toggle(self) -> None:
        """Toggle panel visibility."""
        self.visible = not self.visible

    def update(self) -> None:
        """Update panel state."""
        if not self.visible:
            return

        # Scroll with up/down
        if pyxel.btnp(pyxel.KEY_UP):
            self.scroll = max(0, self.scroll - 1)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.scroll = min(len(self.params) - 1, self.scroll + 1)

        # Adjust values with left/right
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT):
            category, key, label, min_val, max_val, step = self.params[self.scroll]

            current = game_config.get(category, key)

            if pyxel.btn(pyxel.KEY_LEFT):
                new_val = max(min_val, current - step)
            else:
                new_val = min(max_val, current + step)

            game_config.set(category, key, value=new_val)

    def draw(self, screen_width: int, screen_height: int) -> None:
        """
        Draw the beta panel.

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        if not self.visible:
            return

        # Draw semi-transparent background
        pyxel.rect(5, 5, screen_width - 10, screen_height - 10, 1)
        pyxel.rectb(5, 5, screen_width - 10, screen_height - 10, 7)

        # Title
        pyxel.text(10, 10, "BETA PANEL (F1:Close F5:Save F9:Reset)", 7)
        pyxel.text(10, 18, "UP/DOWN: Select  LEFT/RIGHT: Adjust", 6)

        # Draw parameters
        y = 30
        for i, (category, key, label, min_val, max_val, step) in enumerate(self.params):
            value = game_config.get(category, key)

            # Highlight selected
            color = 10 if i == self.scroll else 7

            # Format value based on type
            if isinstance(value, float):
                value_str = f"{value:.2f}"
            else:
                value_str = str(value)

            text = f"{label}: {value_str}"
            pyxel.text(15, y, text, color)

            # Show range
            range_text = f"[{min_val}-{max_val}]"
            pyxel.text(140, y, range_text, 5)

            y += 8

            if y > screen_height - 20:
                break

        # Instructions at bottom
        pyxel.text(10, screen_height - 15, "F5: Save Config", 11)
        pyxel.text(100, screen_height - 15, "F9: Reset to Default", 8)


class HUD:
    """Heads-up display for game info."""

    @staticmethod
    def draw_freshness_indicator(x: float, y: float, fresh: float,
                                 fresh_max: float, show_value: bool) -> None:
        """
        Draw freshness indicator.

        Args:
            x, y: Position
            fresh: Freshness value
            fresh_max: Maximum freshness
            show_value: Whether to show numeric value
        """
        ratio = fresh / fresh_max if fresh_max > 0 else 0

        # Color based on freshness
        if ratio > 0.7:
            color = 11  # Green
        elif ratio > 0.4:
            color = 10  # Yellow
        elif ratio > 0.15:
            color = 9   # Orange
        else:
            color = 8   # Red

        if show_value:
            # Show numeric value (before dropping)
            pyxel.text(x - 8, y - 10, f"{int(fresh)}", color)
        else:
            # Show visual indicator only (after dropping)
            # Draw small sparkles for high freshness
            if ratio > 0.7:
                pyxel.pset(x - 3, y - 5, 7)
                pyxel.pset(x + 3, y - 5, 7)
                pyxel.pset(x, y - 7, 7)

    @staticmethod
    def draw_score_panel(x: int, y: int, score_tracker) -> None:
        """
        Draw score information panel.

        Args:
            x, y: Top-left position
            score_tracker: ScoreTracker instance
        """
        pyxel.rectb(x, y, 110, 55, 7)

        pyxel.text(x + 3, y + 3, "SCORE", 7)
        pyxel.text(x + 3, y + 11, f"{score_tracker.get_score()}", 11)

        pyxel.text(x + 3, y + 21, f"Delivered: {score_tracker.delivered_count}", 7)
        pyxel.text(x + 3, y + 29, f"Rotten: {score_tracker.rotten_count}", 8)

        fresh_eff = score_tracker.get_effective_fresh()
        pyxel.text(x + 3, y + 37, f"Fresh: {int(fresh_eff)}", 10)

        if score_tracker.rotten_count > 0:
            damage = score_tracker.get_rot_damage_percent()
            pyxel.text(x + 3, y + 45, f"Damage: -{damage:.1f}%", 8)
