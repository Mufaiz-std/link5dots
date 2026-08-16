from settings.settings_store import SettingsStore
import os

def test_settings_persistence():
    print("--- Testing Settings Persistence ---")
    
    # Reset file
    if os.path.exists('settings.json'):
        os.remove('settings.json')
        
    s1 = SettingsStore()
    s1._settings = {
        'sound': True,
        'haptics': True,
        'show_last_move': True
    }
    s1.set('sound', False)
    s1.set('haptics', False)
    s1.set('show_last_move', False)
    
    # Simulate app close by re-instantiating store from disk
    s1._instance = None # reset singleton
    s2 = SettingsStore()
    
    assert s2.get('sound') == False
    assert s2.get('haptics') == False
    assert s2.get('show_last_move') == False
    
    print("  OK: Settings persisted correctly across sessions.")

if __name__ == '__main__':
    test_settings_persistence()
