from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QMetaObject
from PyQt5.QtGui import QPainter, QColor, QPen

class SmudgeBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""QProgressBar { 
          background-color: rgba(70, 70, 70, 1); 
          border-radius: 0px; 
        }

        QProgressBar::chunk {
           background-color: rgba(255, 255, 255, 1); 
           border-radius: 0px; 
           width: 1px;
           }
        """)
        self.setRange(0, 180)
        self.setValue(180)
        self.setTextVisible(False)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(self.width() / 2, 0, self.width() / 2, self.height())
        painter.drawLine(self.width() * 2 / 3, 0, self.width() * 2 / 3, self.height())

class SmudgeTimer(QWidget):
    time_updated = pyqtSignal(int)

    def __init__(self, parent=None, total_time=180):
        super().__init__(parent)
        self.total_time = total_time
        self.remaining_time = total_time

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.setInterval(1000)

        self.progress_bar = SmudgeBar(self)
        
        # Add a label for the progress bar
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 16pt;")
        self.label.setText(self.format_time(self.remaining_time))

        # Add the progress bar and label widgets to a container widget
        container = QWidget(self)
        container.setStyleSheet("background-color: rgba(70, 70, 70, 0.3); border-radius: 0px;")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.addWidget(self.progress_bar)
        container_layout.addWidget(self.label)

        # Add the container widget to the layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(container)

    def start(self):
        QMetaObject.invokeMethod(self.timer, "start", Qt.QueuedConnection)

    def stop(self):
        QMetaObject.invokeMethod(self.timer, "stop", Qt.QueuedConnection)

    def reset(self):
        self.remaining_time = self.total_time
        self.progress_bar.setValue(self.remaining_time)
        self.label.setText(self.format_time(self.remaining_time))


    def update_time(self):
        self.remaining_time -= 1
        self.progress_bar.setValue(self.remaining_time)
        self.label.setText(self.format_time(self.remaining_time))
        self.time_updated.emit(self.remaining_time)
        if self.remaining_time == 0:
            self.timer.stop()

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:01d}:{seconds:02d}"