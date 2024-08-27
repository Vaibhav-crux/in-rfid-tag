import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QRectF
from app.ui.titleBar.window_controls import create_minimize_button, create_close_button
from app.ui.mainWindow.mainWindow import FullScreenWindow
from app.ui.login.imageHandler import fetch_and_process_image
from app.ui.login.inRfidWidget import InRfidWidget  # Import the new widget

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window settings
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 500, 400)
        self.setFixedSize(500, 550)  # Fixed size to avoid resizing

        # Apply rounded corners
        self.apply_rounded_corners(20)

        # Center the window on the screen
        self.center_on_screen()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Custom title bar with gradient background
        title_bar = QFrame(self)
        title_bar.setFixedHeight(40)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)

        # Spacer before the title to help center it
        left_spacer = QLabel('', title_bar)
        title_bar_layout.addWidget(left_spacer)

        title_label = QLabel('Login', title_bar)
        title_label.setAlignment(Qt.AlignCenter)
        title_bar_layout.addWidget(title_label)

        # Spacer after the title to help center it
        right_spacer = QLabel('', title_bar)
        title_bar_layout.addWidget(right_spacer)

        # Adjust spacer sizes to achieve perfect centering
        title_bar_layout.setStretch(0, 1)
        title_bar_layout.setStretch(1, 0)
        title_bar_layout.setStretch(2, 1)

        # Add minimize and close buttons
        minimize_button = create_minimize_button(self)
        title_bar_layout.addWidget(minimize_button)

        close_button = create_close_button(self)
        title_bar_layout.addWidget(close_button)

        main_layout.addWidget(title_bar)

        # Content layout
        content_frame = QFrame(self)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setAlignment(Qt.AlignCenter)

        # Image in a circular shape
        image_label = QLabel(self)
        radius = 75
        circular_pixmap = fetch_and_process_image(radius)
        image_label.setPixmap(circular_pixmap)
        image_label.setFixedSize(2 * radius, 2 * radius)
        image_label.setAlignment(Qt.AlignCenter)

        image_layout = QVBoxLayout()
        image_layout.addWidget(image_label)
        image_layout.setAlignment(Qt.AlignCenter)

        # Add InRfidWidget to the content layout
        rfid_widget = InRfidWidget(self)
        content_layout.addLayout(image_layout)
        content_layout.addWidget(rfid_widget)

        main_layout.addWidget(content_frame)
        self.setLayout(main_layout)

        # Set the background color of the window
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  # White background
        self.setPalette(palette)

    def apply_rounded_corners(self, radius):
        """Apply rounded corners to the window."""
        path = QPainterPath()
        rect = QRectF(0, 0, self.width(), self.height())
        path.addRoundedRect(rect, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def center_on_screen(self):
        """Center the window on the screen."""
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def mousePressEvent(self, event):
        # Enable dragging of the window
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # Move window while dragging
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
