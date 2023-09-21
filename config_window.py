import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt

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
        
        self.crosshair_layout = QHBoxLayout()
        self.crosshair_label = QLabel('Toggle Crosshair:')
        self.crosshair_button = QPushButton()
        self.crosshair_layout.addWidget(self.crosshair_label)
        self.crosshair_layout.addWidget(self.crosshair_button)
        layout.addLayout(self.crosshair_layout)
        
        self.settings_layout = QHBoxLayout()
        self.settings_label = QLabel('Show Settings:')
        self.settings_button = QPushButton()
        self.settings_layout.addWidget(self.settings_label)
        self.settings_layout.addWidget(self.settings_button)
        layout.addLayout(self.settings_layout)
        
        self.quit_layout = QHBoxLayout()
        self.quit_label = QLabel('Quit:')
        self.quit_button = QPushButton()
        self.quit_layout.addWidget(self.quit_label)
        self.quit_layout.addWidget(self.quit_button)
        layout.addLayout(self.quit_layout)
        
        self.setLayout(layout)
        
        self.load_current_keybinds()
        
        self.timer_button.clicked.connect(lambda: self.record_keybind('toggle_timer'))
        self.crosshair_button.clicked.connect(lambda: self.record_keybind('toggle_crosshair'))
        self.toggle_button.clicked.connect(lambda: self.record_keybind('toggle_visibility'))
        self.quit_button.clicked.connect(lambda: self.record_keybind('quit'))
        self.settings_button.clicked.connect(lambda: self.record_keybind('toggle_settings'))
        self.update_ui_signal.connect(self.update_ui)
    
    def load_current_keybinds(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.timer_button.setText(self.keybind_manager.chord_to_user_friendly(config['toggle_timer']))
            self.crosshair_button.setText(self.keybind_manager.chord_to_user_friendly(config['toggle_crosshair']))
            self.toggle_button.setText(self.keybind_manager.chord_to_user_friendly(config['toggle_visibility']))
            self.quit_button.setText(self.keybind_manager.chord_to_user_friendly(config['quit']))
            self.settings_button.setText(self.keybind_manager.chord_to_user_friendly(config['toggle_settings']))
    
    @pyqtSlot(str)
    def update_ui(self, chord):
        chord = self.keybind_manager.chord_to_user_friendly(chord)
        if self.current_action == 'toggle_visibility':
            self.toggle_button.setText(chord)
        elif self.current_action == 'toggle_timer':
            self.timer_button.setText(chord)
        elif self.current_action == 'toggle_crosshair':
            self.crosshair_button.setText(chord)
        elif self.current_action == 'quit':
            self.quit_button.setText(chord)
        elif self.current_action == 'toggle_settings':
            self.settings_button.setText(chord)

        self.current_action = None

    def on_record_keybind(self, action, chord):
        self.update_ui_signal.emit(chord)

    def record_keybind(self, action):
        self.current_action = action
        self.keybind_manager.record(action, self.on_record_keybind)
        





