import sys
import os
from PyQt5.QtWidgets import QApplication
from game_overlay import GameOverlay
import signal
import json

def generate_default_config():
    if not os.path.exists('config.json'):
        with open('config.json', 'w') as f:
            json.dump({
              'toggle_timer': 'ctrl+shift+t',
              'toggle_settings': 'ctrl+shift+s', 
              'toggle_visibility': 'ctrl+shift+a', 
              'quit': 'ctrl+shift+q'
              }, f, indent=4)

def signal_handler(signal, frame):
    print("Ctrl+C pressed. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    generate_default_config()

    app = QApplication(sys.argv)

    ex = GameOverlay("Phasmophobia")
    ex.keybind_manager.setup_keybinds(ex)
    
    exit(app.exec_())