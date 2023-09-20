import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QTime, QMutex, QMutexLocker
import ctypes
import keyboard

def generate_default_config():
    if not os.path.exists('config.json'):
        with open('config.json', 'w') as f:
            json.dump({
              'settings': 'ctrl+shift+s', 
              'toggle': 'ctrl+shift+a', 
              'quit': 'ctrl+shift+q'
              }, f, indent=4)

class ConfigWindow(QWidget):
    def __init__(self, game_overlay):
        super().__init__()
        self.game_overlay = game_overlay
        layout = QVBoxLayout()
        
        self.toggle_layout = QHBoxLayout()
        self.toggle_label = QLabel('Toggle Visibility:')
        self.toggle_button = QPushButton()
        self.toggle_layout.addWidget(self.toggle_label)
        self.toggle_layout.addWidget(self.toggle_button)
        layout.addLayout(self.toggle_layout)
        
        self.quit_layout = QHBoxLayout()
        self.quit_label = QLabel('Quit:')
        self.quit_button = QPushButton()
        self.quit_layout.addWidget(self.quit_label)
        self.quit_layout.addWidget(self.quit_button)
        layout.addLayout(self.quit_layout)

        self.settings_layout = QHBoxLayout()
        self.settings_label = QLabel('Show Settings:')
        self.settings_button = QPushButton()
        self.settings_layout.addWidget(self.settings_label)
        self.settings_layout.addWidget(self.settings_button)
        layout.addLayout(self.settings_layout)
        
        self.setLayout(layout)
        
        self.load_current_keybinds()
        
        self.toggle_button.clicked.connect(lambda: self.record_keybind('toggle'))
        self.quit_button.clicked.connect(lambda: self.record_keybind('quit'))
        self.settings_button.clicked.connect(lambda: self.record_keybind('settings'))
    
    def load_current_keybinds(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.toggle_button.setText(config['toggle'])
            self.quit_button.setText(config['quit'])
            self.settings_button.setText(config['settings'])
    
    def record_keybind(self, action):
        recorded_events = keyboard.record(until='esc')
        chord = '+'.join([event.name for event in recorded_events if event.event_type == 'down'])
        with open('config.json', 'r+') as f:
            config = json.load(f)
            config[action] = chord
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()
        if action == 'toggle':
            self.toggle_button.setText(chord)
        elif action == 'quit':
            self.quit_button.setText(chord)
        elif action == 'settings':
            self.settings_button.setText(chord)
        self.game_overlay.setup_keybinds()

class GameOverlay(QWidget):
    def __init__(self, target_executable_name):
        super().__init__()
        self.target_executable_name = target_executable_name
        self.target_window = None

        self.config_window = ConfigWindow(self)
        self.active_hotkeys = set()

        # Set the window to be transparent and always on top
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowTransparentForInput)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_target_window)
        self.timer.start(1000)  # Check every second

        # Set up a QTime to keep track of the elapsed time
        self.time_elapsed = QTime(0, 0)

        self.settings_mutex = QMutex()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw a red rectangle at the top right of the window
        painter.setBrush(QColor(255, 0, 0))
        painter.drawRect(self.width() - 120, 20, 100, 50)

    def check_target_window(self):
        hwnd = ctypes.windll.user32.FindWindowW(None, self.target_executable_name)
        if hwnd:
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            self.setGeometry(rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)
            self.show()
            self.timer.stop()
        else:
            self.time_elapsed = self.time_elapsed.addSecs(1)
            if self.time_elapsed >= QTime(0, 2):  # 2 minutes
                self.timer.stop()
                QMessageBox.information(self, "Game Not Found", "The Phasmophobia game was not found within the specified time (2 minutes).")
                self.quit_application()

    def settings_action(self):
        # Use a QMutexLocker to automatically lock and unlock the mutex
        locker = QMutexLocker(self.settings_mutex)
        
        if self.config_window.isVisible():
            self.config_window.hide()
        else:
            self.config_window.show()


    def toggle_action(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def quit_action(self):
        self.close()
        self.config_window.close()
        exit()
        
        
    def setup_keybinds(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            
            new_hotkeys = {
                'settings': config['settings'],
                'toggle': config['toggle'],
                'quit': config['quit']
            }

            for action, hotkey in new_hotkeys.items():
                if hotkey in self.active_hotkeys:
                    keyboard.clear_hotkey(hotkey)
                    self.active_hotkeys.remove(hotkey)

                keyboard.add_hotkey(hotkey, getattr(self, f"{action}_action"))
                self.active_hotkeys.add(hotkey)

import signal

def signal_handler(signal, frame):
    print("Ctrl+C pressed. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    generate_default_config()

    app = QApplication(sys.argv)

    ex = GameOverlay("Phasmophobia")
    ex.setup_keybinds()
    
    exit(app.exec_())