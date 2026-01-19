"""Title scene with game instructions."""
import pyxel


class TitleScene:
    """Title screen scene."""

    def __init__(self, app):
        """
        Initialize title scene.

        Args:
            app: Main application instance
        """
        self.app = app

    def update(self) -> None:
        """Update title scene."""
        # Start game on space or click
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.app.change_scene("play")

        # Quit on Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self) -> None:
        """Draw title scene."""
        pyxel.cls(0)

        # Title
        title = "WAKAYAMA MIKAN"
        pyxel.text(pyxel.width // 2 - len(title) * 2, 20, title, 10)

        subtitle = "Delivery Game (BETA)"
        pyxel.text(pyxel.width // 2 - len(subtitle) * 2, 30, subtitle, 7)

        # Instructions
        y = 50
        instructions = [
            "HOW TO PLAY:",
            "",
            "- Move mouse to position fruit",
            "- Click to drop",
            "- Merge same fruits",
            "- Create MIKAN to deliver",
            "",
            "FRESHNESS SYSTEM:",
            "- High fresh = high score",
            "- Fresh decays over time",
            "- Merge recovers fresh!",
            "- Rotten mikan damage score",
            "",
            "CONTROLS:",
            "- Mouse: Position",
            "- Click: Drop",
            "- ESC: Pause",
            "- S: Ship out (end game)",
            "",
            "BETA FEATURES:",
            "- F1: Adjustment panel",
            "- F5: Save config",
            "- F9: Reset to default",
            "",
            "Press SPACE or CLICK to start",
        ]

        for line in instructions:
            if line.startswith("-"):
                pyxel.text(20, y, line, 6)
            elif line.endswith(":"):
                pyxel.text(20, y, line, 11)
            elif line:
                pyxel.text(20, y, line, 7)
            y += 7

        # Version
        pyxel.text(5, pyxel.height - 8, "v0.1 Beta", 5)
