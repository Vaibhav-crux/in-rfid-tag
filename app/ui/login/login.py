import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from app.ui.titleBar.window_controls import create_minimize_button, create_close_button
from app.ui.mainWindow.mainWindow import FullScreenWindow
from app.ui.login.imageHandler import fetch_and_process_image

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def load_stylesheet(self, file_path):
        """Utility function to load and return a stylesheet."""
        with open(file_path, "r") as file:
            return file.read()

    def initUI(self):
        # Remove the default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 500, 400)
        self.setFixedSize(500, 400)  # Fixed size to avoid resizing

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

        # Rest of the UI
        content_frame = QFrame(self)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setAlignment(Qt.AlignCenter)

        # Image in a circular shape
        image_label = QLabel(self)

        # Use the fetch_and_process_image function
        radius = 75  # Radius of the circle
        circular_pixmap = fetch_and_process_image(radius)

        image_label.setPixmap(circular_pixmap)
        image_label.setFixedSize(2 * radius, 2 * radius)
        image_label.setAlignment(Qt.AlignCenter)

        # Center the image in the window
        image_layout = QVBoxLayout()
        image_layout.addWidget(image_label)
        image_layout.setAlignment(Qt.AlignCenter)

        # Right side with login form
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        # Load and apply stylesheets
        email_label = QLabel('Enter your User Id:', self)
        email_label.setFont(QFont('Arial', 12, QFont.Bold))  # Apply font directly
        self.email_entry = QLineEdit(self)
        self.email_entry.setFixedHeight(35)
        self.email_entry.setStyleSheet(self.load_stylesheet('app/stylesheet/login/lineEdit.qss'))
        self.email_entry.setPlaceholderText("UserId")
        self.email_entry.setFocus()

        password_label = QLabel('Password:', self)
        password_label.setFont(QFont('Arial', 12, QFont.Bold))  # Apply font directly
        self.password_entry = QLineEdit(self)
        self.password_entry.setFixedHeight(35)
        self.password_entry.setStyleSheet(self.load_stylesheet('app/stylesheet/login/lineEdit.qss'))
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Password")

        self.login_button = QPushButton('Login', self)
        self.login_button.setStyleSheet(self.load_stylesheet('app/stylesheet/login/button.qss'))

        # Connect the login button to the open_fullscreen_window method
        self.login_button.clicked.connect(self.open_fullscreen_window)

        # Arrange the widgets in the form layout
        form_layout.addLayout(image_layout)
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_entry)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_entry)
        form_layout.addWidget(self.login_button)

        content_layout.addLayout(form_layout)
        main_layout.addWidget(content_frame)

        self.setLayout(main_layout)

        # Set the background color of the window
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  # White background
        self.setPalette(palette)

        # Connect Enter key press events
        self.email_entry.returnPressed.connect(self.focus_password_entry)
        self.password_entry.returnPressed.connect(self.trigger_login)

    def center_on_screen(self):
        """Center the window on the screen."""
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def focus_password_entry(self):
        """Move focus to the password entry when Enter is pressed in the email entry."""
        self.password_entry.setFocus()

    def trigger_login(self):
        """Trigger the login button when Enter is pressed in the password entry."""
        self.login_button.click()

    def open_fullscreen_window(self):
        """Open the full-screen window when the login button is clicked."""
        self.full_screen_window = FullScreenWindow()
        self.full_screen_window.show()
        self.close()  # Close the login window

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
