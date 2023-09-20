import json
import keyboard

class KeybindManager:
    def __init__(self):
        self.active_hotkeys = set()
        self.load_config()

    def load_config(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)

    def update_config(self, action, chord):
        self.config[action] = chord
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def setup_keybinds(self, target):
        keyboard.unhook_all()
        for action, hotkey in self.config.items():
            keyboard.add_hotkey(hotkey, getattr(target, f"{action}_action"))
