# app/ui/mainWindow/timeSection.py

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QFont

def create_clock_frame(parent):
    """Creates and returns the digital clock frame."""
    clock_frame = QFrame(parent)
    clock_frame.setFrameShape(QFrame.StyledPanel)
    clock_frame.setStyleSheet("""
        QFrame {
            background-color: #34495e;
            border-radius: 10px;
            padding: 10px;
            color: white;
        }
        QLabel {
            color: white;
            font-size: 24px;
        }
    """)
    clock_layout = QVBoxLayout(clock_frame)
    clock_layout.setContentsMargins(10, 10, 10, 10)

    # Create clock label
    clock_label = QLabel()
    clock_label.setAlignment(Qt.AlignCenter)
    clock_label.setFont(QFont("Arial", 24))
    clock_layout.addWidget(clock_label)

    # Update the clock every second
    timer = QTimer(parent)
    timer.timeout.connect(lambda: update_clock(clock_label))
    timer.start(1000)  # Update every second

    return clock_frame

def update_clock(label):
    """Updates the clock label with the current time and date."""
    current_time = QTime.currentTime().toString("HH:mm:ss")
    current_date = QDate.currentDate().toString("dddd, MMMM d, yyyy")
    label.setText(f"{current_time}\n{current_date}")
