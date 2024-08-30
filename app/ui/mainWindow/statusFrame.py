# app/ui/mainWindow/statusFrame.py

from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

def create_status_frame(vehicle_info):
    """Creates and returns the status frame."""
    status_frame = QFrame()
    status_frame.setFrameShape(QFrame.StyledPanel)
    status_frame.setStyleSheet("""
        QFrame {
            background-color: #34495e;
            border-radius: 10px;
            padding: 10px;
            color: white;
        }
        QLabel {
            color: white;
            font-size: 18px;
        }
    """)
    status_layout = QHBoxLayout(status_frame)
    status_layout.setContentsMargins(10, 10, 10, 10)

    # Status label (inside the frame)
    vehicle_info['statusLabel'] = QLabel("Waiting")
    vehicle_info['statusLabel'].setFont(QFont("Arial", 16, QFont.Bold))
    status_layout.addWidget(vehicle_info['statusLabel'], alignment=Qt.AlignLeft)

    # Indicator label
    vehicle_info['indicatorLabel'] = QLabel()
    vehicle_info['indicatorLabel'].setFixedSize(20, 20)
    vehicle_info['indicatorLabel'].setStyleSheet("background-color: grey; border-radius: 10px;")
    status_layout.addWidget(vehicle_info['indicatorLabel'])

    status_layout.addStretch()  # Add stretch to push content to the left

    return status_frame
