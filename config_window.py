import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
import keyboard

class ConfigWindow(QWidget):
    update_ui_signal = pyqtSignal(str)
    def __init__(self, game_overlay, keybind_manager):
        super().__init__()
        self.game_overlay = game_overlay
        self.keybind_manager = keybind_manager

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        layout = QVBoxLayout()
        
        self.timer_layout = QHBoxLayout()
        self.timer_label = QLabel('Toggle Timer:')
        self.timer_button = QPushButton()
        self.timer_layout.addWidget(self.timer_label)
        self.timer_layout.addWidget(self.timer_button)
        layout.addLayout(self.timer_layout)

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
        
        self.timer_button.clicked.connect(lambda: self.record_keybind('toggle_timer'))
        self.toggle_button.clicked.connect(lambda: self.record_keybind('toggle_visibility'))
        self.quit_button.clicked.connect(lambda: self.record_keybind('quit'))
        self.settings_button.clicked.connect(lambda: self.record_keybind('toggle_settings'))
        self.update_ui_signal.connect(self.update_ui)
    
    def load_current_keybinds(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.timer_button.setText(config['toggle_timer'])
            self.toggle_button.setText(config['toggle_visibility'])
            self.quit_button.setText(config['quit'])
            self.settings_button.setText(config['toggle_settings'])
    
    @pyqtSlot(str)
    def update_ui(self, chord):
        if self.current_action == 'toggle_visibility':
            self.toggle_button.setText(chord)
        elif self.current_action == 'toggle_timer':
            self.timer_button.setText(chord)
        elif self.current_action == 'quit':
            self.quit_button.setText(chord)
        elif self.current_action == 'toggle_settings':
            self.settings_button.setText(chord)
        

    def record_keybind(self, action):
        self.current_action = action
        control_keys = {'ctrl', 'shift', 'alt', 'cmd', 'windows'}
        key_chord = set()

        def on_key_event(event):
            nonlocal key_chord
            if event.event_type == 'down':
                key_chord.add(event.name)
                if event.name not in control_keys:
                    keyboard.unhook_all()
                    
                    # Separate control keys and other keys
                    ctrl_key = 'ctrl' if 'ctrl' in key_chord else ''
                    alt_key = 'alt' if 'alt' in key_chord else ''
                    shift_key = 'shift' if 'shift' in key_chord else ''
                    other_keys = [key for key in key_chord if key not in control_keys]
                    
                    # Construct chord_str with control keys in the specified order
                    chord_str = '+'.join(filter(None, [ctrl_key, alt_key, shift_key] + other_keys))
                    
                    config = self.game_overlay.keybind_manager.config
                    config[action] = chord_str
                    self.keybind_manager.update_config(action, chord_str)
                    self.keybind_manager.setup_keybinds(self.game_overlay)
                    self.update_ui_signal.emit(chord_str)

        keyboard.hook(on_key_event)





