"""Main application with Pyxel initialization and scene management."""
import pyxel
from game.scene_title import TitleScene
from game.scene_play import PlayScene
from game.scene_result import ResultScene


class App:
    """Main application class."""

    # Screen dimensions
    WIDTH = 256
    HEIGHT = 256

    def __init__(self):
        """Initialize the application."""
        # Initialize Pyxel
        pyxel.init(self.WIDTH, self.HEIGHT, title="Wakayama Mikan Delivery (Beta)")
        pyxel.mouse(True)

        # Initialize scenes
        self.scenes = {
            "title": TitleScene(self),
            "play": PlayScene(self),
            "result": ResultScene(self),
        }

        self.current_scene_name = "title"

    def change_scene(self, scene_name: str) -> None:
        """
        Change to a different scene.

        Args:
            scene_name: Name of scene to switch to
        """
        if scene_name in self.scenes:
            self.current_scene_name = scene_name

            # Reset play scene when entering
            if scene_name == "play":
                self.scenes["play"].reset()

    def update(self) -> None:
        """Update current scene."""
        current_scene = self.scenes[self.current_scene_name]
        current_scene.update()

    def draw(self) -> None:
        """Draw current scene."""
        current_scene = self.scenes[self.current_scene_name]
        current_scene.draw()

    def run(self) -> None:
        """Start the application."""
        pyxel.run(self.update, self.draw)
