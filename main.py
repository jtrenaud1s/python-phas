import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtCore import QTime, QTimer, QRect
from game_overlay import GameOverlay
import signal
import json

class PhasOverlay(QWidget):
    overlay = None

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_target_window)
        self.timer.start(1000)  # Check every second
        self.time_elapsed = QTime(0, 0)
        

    def check_target_window(self):
            hwnd = ctypes.windll.user32.FindWindowW(None, "Phasmophobia")
            if hwnd:
                rect = ctypes.wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                self.overlay = GameOverlay(rect)
                self.overlay.show()
                self.timer.stop()
            else:
                self.time_elapsed = self.time_elapsed.addSecs(1)
                if self.time_elapsed >= QTime(0, 2):  # 2 minutes
                    self.timer.stop()
                    QMessageBox.information(self, "Game Not Found", "The Phasmophobia game was not found within the specified time (2 minutes).")
                    self.quit_application()


def generate_default_config():
    if not os.path.exists('config.json'):
        with open('config.json', 'w') as f:
            json.dump({
              'toggle_timer': 't',
              'toggle_crosshair': 'ctrl_l+shift+c',
              'toggle_settings': 'ctrl_l+shift+s', 
              'toggle_visibility': 'ctrl_l+shift+a', 
              'quit': 'ctrl_l+shift+q'
              }, f, indent=4)

def signal_handler(signal, frame):
    print("Ctrl+C pressed. Exiting...")
    sys.exit(0)


if __name__ == '__main__':
    generate_default_config()
    signal.signal(signal.SIGINT, signal_handler)

    app = QApplication(sys.argv)
    phasOverlay = PhasOverlay()
    
    sys.exit(app.exec_())