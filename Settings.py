import json
import os
from typing import Dict, Any

class Settings:
    def __init__(self):
        self.settings_file = 'settings.json'
        self.default_settings = {
            'grid_size': 4,
            'sound_enabled': True,
            'dark_mode': False,
            'scores': []
        }
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from file or create with defaults if file doesn't exist."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Ensure all default settings exist
                    for key, value in self.default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
            except (json.JSONDecodeError, IOError):
                return self.default_settings.copy()
        else:
            # Create settings file with defaults
            self.save_settings(self.default_settings)
            return self.default_settings.copy()

    def save_settings(self, settings):
        """Save settings to file."""
        try:
            # Open file in write mode
            f = open(self.settings_file, 'w')
            # Write settings
            json.dump(settings, f, indent=4)
            # Force file system sync
            f.flush()
            os.fsync(f.fileno())
            # Close file
            f.close()
        except IOError:
            pass  # Handle file write errors silently

    def get_setting(self, key, default=None):
        """Get a setting value."""
        # Always read from file to ensure latest value
        settings = self.load_settings()
        return settings.get(key, default)

    def set_setting(self, key, value):
        """Set a setting value and save to file."""
        # Load current settings
        settings = self.load_settings()
        # Update setting
        settings[key] = value
        # Save to file
        self.save_settings(settings)
        # Update local cache
        self.settings = settings

    def reset_settings(self):
        """Reset all settings to defaults."""
        self.settings = self.default_settings.copy()
        self.save_settings(self.settings)

    def add_score(self, name: str, moves: int, time: int) -> None:
        """Add a new score to the scoreboard."""
        scores = self.settings.get('scores', [])
        scores.append({
            'name': name,
            'moves': moves,
            'time': time
        })
        # Keep only top 10 scores
        scores.sort(key=lambda x: (x['moves'], x['time']))
        self.settings['scores'] = scores[:10]
        self.save_settings(self.settings)

    def clear_scores(self) -> None:
        """Clear all scores."""
        self.settings['scores'] = []
        self.save_settings(self.settings)

    def get_scores(self) -> list:
        """Get all scores."""
        return self.settings.get('scores', []) 