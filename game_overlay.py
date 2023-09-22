import ctypes
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QTime, QMetaObject
from config_window import ConfigWindow
from keybind_manager import KeybindManager
from smudge_timer import SmudgeTimer
from crosshair import Crosshair


class GameOverlay(QWidget):
    def __init__(self, rect):
        super().__init__()
        self.keybind_manager = KeybindManager(self)
        
        # Set the window to be transparent and always on top
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowTransparentForInput)

        self.setGeometry(rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)

        # Set up a QTime to keep track of the elapsed time
        self.time_elapsed = QTime(0, 0)

        # Create the SmudgeTimer widget
        self.countdown_timer = SmudgeTimer(self, 180)
        self.crosshair = Crosshair(self)
        self.crosshair.setGeometry(int(self.width() / 2) - 3, int(self.height() / 2) - 3, 11, 11)

        # Add the SmudgeTimer widget to the layout
        self.countdown_timer.setGeometry(0, 0, 400, 125)
        self.countdown_timer.move(self.width() - self.countdown_timer.width(), 0)

        self.config_window = ConfigWindow(self, self.keybind_manager)


    def toggle_settings_action(self):  
        if self.config_window.isVisible():
            QMetaObject.invokeMethod(self.config_window, "hide", Qt.QueuedConnection) 
        else:
            QMetaObject.invokeMethod(self.config_window, "show", Qt.QueuedConnection) 

    def toggle_timer_action(self):
        if self.countdown_timer.timer.isActive():
            self.countdown_timer.stop()
        else:
            self.countdown_timer.reset()
            self.countdown_timer.start()


    def toggle_visibility_action(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
    
    def toggle_crosshair_action(self):
        self.crosshair.toggle_crosshair()

    def quit_action(self):
        self.close()
        self.config_window.close()
        exit()
        
  