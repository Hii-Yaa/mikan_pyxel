"""Result scene showing final score."""
import pyxel


class ResultScene:
    """Result screen scene."""

    def __init__(self, app):
        """
        Initialize result scene.

        Args:
            app: Main application instance
        """
        self.app = app
        self.score_tracker = None
        self.game_over_reason = ""

    def set_result(self, score_tracker, reason: str) -> None:
        """
        Set result data.

        Args:
            score_tracker: ScoreTracker with final scores
            reason: Game over reason
        """
        self.score_tracker = score_tracker
        self.game_over_reason = reason

    def update(self) -> None:
        """Update result scene."""
        # Return to title on space or click
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.app.change_scene("title")

        # Quit on Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self) -> None:
        """Draw result scene."""
        pyxel.cls(0)

        if not self.score_tracker:
            return

        # Title
        pyxel.text(pyxel.width // 2 - 20, 20, "GAME OVER", 8)
        pyxel.text(pyxel.width // 2 - 30, 30, self.game_over_reason, 7)

        # Score
        score = self.score_tracker.get_score()
        score_text = f"FINAL SCORE: {score}"
        pyxel.text(pyxel.width // 2 - len(score_text) * 2, 50, score_text, 11)

        # Details
        y = 70
        details = [
            ("Mikan Delivered:", self.score_tracker.delivered_count, 10),
            ("Rotten Mikan:", self.score_tracker.rotten_count, 8),
            ("", "", 0),
            ("Total Freshness:", int(self.score_tracker.fresh_sum), 7),
            ("Effective Fresh:", int(self.score_tracker.get_effective_fresh()), 11),
        ]

        for label, value, color in details:
            if label:
                text = f"{label} {value}"
                pyxel.text(30, y, text, color)
            y += 10

        # Rot damage
        if self.score_tracker.rotten_count > 0:
            damage = self.score_tracker.get_rot_damage_percent()
            pyxel.text(30, y, f"Rot Damage: -{damage:.1f}%", 8)
            y += 10

        # Performance evaluation
        y += 10
        if self.score_tracker.rotten_count == 0:
            pyxel.text(40, y, "PERFECT! No rotten mikan!", 11)
        elif self.score_tracker.rotten_count <= 2:
            pyxel.text(40, y, "Good job! Very fresh!", 10)
        elif damage < 30:
            pyxel.text(40, y, "Not bad, but watch freshness", 9)
        else:
            pyxel.text(40, y, "Too much rot! Merge faster!", 8)

        # Return instruction
        pyxel.text(pyxel.width // 2 - 40, pyxel.height - 20,
                  "Press SPACE to continue", 7)
