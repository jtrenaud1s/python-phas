import ctypes
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QTime, QMetaObject
from config_window import ConfigWindow
from keybind_manager import KeybindManager


class GameOverlay(QWidget):
    def __init__(self, target_executable_name):
        super().__init__()
        self.target_executable_name = target_executable_name
        self.target_window = None
        self.keybind_manager = KeybindManager()
        
        self.config_window = ConfigWindow(self, self.keybind_manager)

        # Set the window to be transparent and always on top
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowTransparentForInput)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_target_window)
        self.timer.start(1000)  # Check every second

        # Set up a QTime to keep track of the elapsed time
        self.time_elapsed = QTime(0, 0)

        self.total_time = 180  # 3 minutes in seconds
        self.remaining_time = self.total_time

        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_timer_progress)
        self.countdown_timer.setInterval(1000)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw a translucent gray rectangle as a container
        painter.setBrush(QColor(128, 128, 128, 128))  # Translucent gray color
        container_width = 200  # Adjust as needed
        container_height = 75  # Adjust as needed
        container_x = self.width() - container_width - 20  # Adjust as needed for padding
        container_y = 20  # Adjust as needed for padding
        painter.drawRect(container_x, container_y, container_width, container_height)

        # Draw the progress bar background
        painter.setBrush(QColor(70, 70, 70))  # Dark gray color
        progress_bar_width = container_width - 20  # Adjust as needed for padding
        progress_bar_height = 20  # Adjust as needed
        progress_bar_x = container_x + 10  # Adjust as needed for padding
        progress_bar_y = container_y + 15  # Adjust as needed for padding
        painter.drawRect(progress_bar_x - 1, progress_bar_y - 1, progress_bar_width + 2, progress_bar_height + 2)

        # Draw the progress bar
        painter.setBrush(QColor(255, 255, 255))  # White color
        progress_percentage = self.remaining_time / 180  # Assuming timer_value is in seconds and max time is 3 minutes
        progress_bar_current_width = progress_percentage * progress_bar_width
        painter.drawRect(progress_bar_x, progress_bar_y, progress_bar_current_width, progress_bar_height)

        # Draw vertical lines at 2/3 and 1/2 marks

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)  # White color
        painter.drawLine(progress_bar_x + (2/3 * progress_bar_width), progress_bar_y, progress_bar_x + (2/3 * progress_bar_width), progress_bar_y + progress_bar_height)
        painter.drawLine(progress_bar_x + (1/2 * progress_bar_width), progress_bar_y, progress_bar_x + (1/2 * progress_bar_width), progress_bar_y + progress_bar_height)

        minutes, seconds = divmod(self.remaining_time, 60)
        time_text = f"{minutes:02d}:{seconds:02d}"
        
        # Set a larger font
        font = painter.font()
        font.setPointSize(16)  # Set a larger font size
        painter.setFont(font)
        
        
        text_width = painter.fontMetrics().width(time_text)
        text_x = container_x + (container_width - text_width) / 2
        text_y = progress_bar_y + progress_bar_height + 30  # Adjust as needed for padding
        painter.setPen(QColor(255, 255, 255))  # White color
        painter.drawText(text_x, text_y, time_text)

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

    def toggle_settings_action(self):  
        if self.config_window.isVisible():
            QMetaObject.invokeMethod(self.config_window, "hide", Qt.QueuedConnection)      
        else:
            QMetaObject.invokeMethod(self.config_window, "show", Qt.QueuedConnection)      

    def update_timer_progress(self):
        if self.timer_started:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                self.remaining_time = 0
                self.timer.stop()
            self.update()  # Update the UI to redraw the progress bar

    def toggle_timer_action(self):
        if self.countdown_timer.isActive():
            QMetaObject.invokeMethod(self.countdown_timer, "stop", Qt.QueuedConnection) 
            self.timer_started = False
        else:
            QMetaObject.invokeMethod(self.countdown_timer, "start", Qt.QueuedConnection) 
            self.remaining_time = self.total_time
            self.timer_started = True


    def toggle_visibility_action(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def quit_action(self):
        self.close()
        self.config_window.close()
        exit()
        
  