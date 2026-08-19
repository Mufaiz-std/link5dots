import json
import os

class SettingsStore:
    _instance = None
    _filename = 'settings.json'
    
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
            cls._instance._filepath = cls._filename
            cls._instance.load()
        return cls._instance

    def _get_filepath(self):
        """Return a writable path for settings.json.
        On Android, the CWD is not writable so we use Kivy's user_data_dir."""
        try:
            from kivy.app import App
            app = App.get_running_app()
            if app and hasattr(app, 'user_data_dir'):
                return os.path.join(app.user_data_dir, self._filename)
        except Exception:
            pass
        return self._filename

    def load(self):
        filepath = self._get_filepath()
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self._settings.update(data)
            except Exception:
                pass  # use defaults if corrupted

    def save(self):
        filepath = self._get_filepath()
        try:
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            with open(filepath, 'w') as f:
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
