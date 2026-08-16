import json
import os

class SettingsStore:
    _instance = None
    _filepath = 'settings.json'
    
    # Defaults
    _settings = {
        'theme': 'light',
        'sound': True,
        'haptics': True,
        'show_last_move': True,
        'allow_undo': True
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsStore, cls).__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self):
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, 'r') as f:
                    data = json.load(f)
                    self._settings.update(data)
            except Exception:
                pass # use defaults if corrupted

    def save(self):
        try:
            with open(self._filepath, 'w') as f:
                json.dump(self._settings, f)
        except Exception:
            pass

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        self._settings[key] = value
        self.save()

# Global singleton
settings = SettingsStore()
