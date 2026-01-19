"""Configuration management for the game."""
import json
import os
from pathlib import Path
from typing import Any, Dict


class GameConfig:
    """Manages game configuration with load/save functionality."""

    DEFAULT_CONFIG_PATH = "config/game_config.json"

    def __init__(self):
        """Initialize with default configuration."""
        self.config: Dict[str, Any] = {}
        self.config_path = self.DEFAULT_CONFIG_PATH
        self.load()

    def load(self, path: str = None) -> None:
        """Load configuration from JSON file."""
        if path:
            self.config_path = path

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {self.config_path}, using defaults")
            self._load_defaults()
        except json.JSONDecodeError as e:
            print(f"Error parsing config: {e}, using defaults")
            self._load_defaults()

    def save(self, path: str = None) -> None:
        """Save current configuration to JSON file."""
        save_path = path or self.config_path

        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"Configuration saved to {save_path}")
        except Exception as e:
            print(f"Error saving config: {e}")

    def _load_defaults(self) -> None:
        """Load hardcoded default configuration."""
        self.config = {
            "freshness": {
                "fresh_max": 100,
                "spawn_distribution": "triangular",
                "spawn_min": 50,
                "spawn_max": 100,
                "decay_base": 2.0,
                "decay_stage_mult": 1.2,
                "merge_bonus": 20,
                "fresh_cap": 100
            },
            "rot": {
                "rotten_threshold": 30,
                "rot_rate": 0.08
            },
            "score": {
                "fresh_to_score": 1.0,
                "count_bonus": 40
            },
            "game_over": {
                "line_y": 0.2,
                "grace_ms": 3000
            },
            "physics": {
                "gravity": 300.0,
                "bounce": 0.3,
                "friction": 0.98,
                "merge_cooldown": 0.5
            },
            "fruits": [
                {"name": "ume", "display_name": "梅", "radius": 12, "color": 10},
                {"name": "kaki", "display_name": "柿", "radius": 16, "color": 9},
                {"name": "momo", "display_name": "桃", "radius": 20, "color": 8},
                {"name": "budou", "display_name": "ぶどう", "radius": 24, "color": 5},
                {"name": "dekopon", "display_name": "デコポン", "radius": 28, "color": 4},
                {"name": "mikan", "display_name": "みかん", "radius": 32, "color": 10}
            ]
        }

    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults without saving."""
        self._load_defaults()
        print("Configuration reset to defaults (not saved)")

    def get(self, *keys, default=None) -> Any:
        """Get nested configuration value."""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, *keys, value) -> None:
        """Set nested configuration value."""
        if not keys:
            return

        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value


# Global config instance
game_config = GameConfig()
