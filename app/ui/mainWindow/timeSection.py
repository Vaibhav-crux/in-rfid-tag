# app/ui/mainWindow/timeSection.py

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, QDate
from PyQt5.QtGui import QFont
from app.function.shiftTiming.shiftTiming import get_current_shift
from app.function.user.user_info import get_current_user

def create_clock_frame(parent):
    """Creates and returns the digital clock frame with User Name and Shift labels."""
    user_name = get_current_user()

    clock_frame = QFrame(parent)
    clock_frame.setFrameShape(QFrame.StyledPanel)
    clock_frame.setStyleSheet("""
        QFrame {
            background-color: #2c3e50;  /* Darker background for contrast */
            border-radius: 10px;
            padding: 15px;
            color: white;
        }
        QLabel {
            color: #ecf0f1;  /* Light grey color for labels */
            font-size: 18px;
        }
    """)

    clock_layout = QVBoxLayout(clock_frame)
    clock_layout.setContentsMargins(15, 15, 15, 15)  # Increased padding for a more spacious layout
    clock_layout.setSpacing(10)  # Spacing between different sections

    # Create user name layout
    user_layout = QHBoxLayout()
    user_label = QLabel("User Name:")
    user_label.setFont(QFont("Arial", 16, QFont.Bold))
    user_label.setStyleSheet("color: #bdc3c7;")  # Lighter grey for label
    user_value = QLabel(user_name)
    user_value.setFont(QFont("Arial", 24))
    user_value.setStyleSheet("color: #9b59b6;")  # Purple color for user name value
    user_layout.addWidget(user_label)
    user_layout.addWidget(user_value)

    # Create time layout
    time_layout = QHBoxLayout()
    time_label = QLabel("Time:")
    time_label.setFont(QFont("Arial", 16, QFont.Bold))
    time_label.setStyleSheet("color: #bdc3c7;")  # Lighter grey for label
    time_value = QLabel()
    time_value.setFont(QFont("Arial", 24))
    time_value.setStyleSheet("color: #e74c3c;")  # Red color for time value
    time_layout.addWidget(time_label)
    time_layout.addWidget(time_value)
    
    # Create date layout
    date_layout = QHBoxLayout()
    date_label = QLabel("Date:")
    date_label.setFont(QFont("Arial", 16, QFont.Bold))
    date_label.setStyleSheet("color: #bdc3c7;")
    date_value = QLabel()
    date_value.setFont(QFont("Arial", 24))
    date_value.setStyleSheet("color: #3498db;")  # Blue color for date value
    date_layout.addWidget(date_label)
    date_layout.addWidget(date_value)

    # Create day layout
    day_layout = QHBoxLayout()
    day_label = QLabel("Day:")
    day_label.setFont(QFont("Arial", 16, QFont.Bold))
    day_label.setStyleSheet("color: #bdc3c7;")
    day_value = QLabel()
    day_value.setFont(QFont("Arial", 24))
    day_value.setStyleSheet("color: #2ecc71;")  # Green color for day value
    day_layout.addWidget(day_label)
    day_layout.addWidget(day_value)

    # Create shift layout
    shift_layout = QHBoxLayout()
    shift_label = QLabel("Shift:")
    shift_label.setFont(QFont("Arial", 16, QFont.Bold))
    shift_label.setStyleSheet("color: #bdc3c7;")  # Lighter grey for label
    shift_value = QLabel()
    shift_value.setFont(QFont("Arial", 24))
    shift_value.setStyleSheet("color: #f39c12;")  # Orange color for shift value
    shift_layout.addWidget(shift_label)
    shift_layout.addWidget(shift_value)

    # Add layouts to the main clock layout
    clock_layout.addLayout(user_layout)
    clock_layout.addLayout(date_layout)
    clock_layout.addLayout(time_layout)
    clock_layout.addLayout(day_layout)
    clock_layout.addLayout(shift_layout)

    # Update the clock every second, now including shift
    timer = QTimer(parent)
    timer.timeout.connect(lambda: update_clock(time_value, date_value, day_value, shift_value))
    timer.start(1000)  # Update every second

    return clock_frame

def update_clock(time_label, date_label, day_label, shift_label):
    """Updates the clock labels with the current time, date, day, and shift."""
    current_time = QTime.currentTime().toString("HH:mm:ss")
    current_date = QDate.currentDate().toString("MMMM d, yyyy")
    current_day = QDate.currentDate().toString("dddd")
    
    time_label.setText(current_time)
    date_label.setText(current_date)
    day_label.setText(current_day)

    # Fetch and set the current shift
    shift_name = get_current_shift()
    shift_label.setText(shift_name)
