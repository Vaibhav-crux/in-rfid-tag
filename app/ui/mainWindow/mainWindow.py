import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from .title_bar import create_title_bar
from .image_label import create_image_label
from .leftLayout import create_left_form_layout
from .rightLayout import create_right_form_layout
from .fetchDataFromFile import initialize_rfid_monitoring
from .timeSection import create_clock_frame

class FullScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.vehicle_info = {}
        self.setup_ui()

    def load_stylesheet(self, file_path):
        """Utility function to load and return a stylesheet."""
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Stylesheet file not found: {file_path}")
            return ""

    def setup_ui(self):
        """Main UI setup method."""
        # Apply the stylesheet
        stylesheet = self.load_stylesheet("app/stylesheet/mainWindow/mainWindow.qss")
        self.setStyleSheet(stylesheet)

        # Remove the default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()  # Change this to showFullScreen()

        # Main layout with margins
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 0, 20, 10)  # Add margins: left, top, right, bottom
        main_layout.setSpacing(10)  # Add spacing between elements
        self.setLayout(main_layout)  # Set the layout for the window

        # Create custom title bar and add to layout
        title_bar_frame = create_title_bar(self)
        main_layout.addWidget(title_bar_frame)

        # Create the content layout
        content_layout = self.create_content_layout()
        main_layout.addLayout(content_layout)

        # Add the copyright notice below the buttons in two lines
        copyright_label_line1 = QLabel("Copyright laws vary around the world, and there is no global version of copyright,", self)
        copyright_label_line2 = QLabel("but many countries are part of the Starlabs Technologo Pvt. Ltd., which deals with protecting original works and the authors’ rights over them.", self)

        # Center align the text
        copyright_label_line1.setAlignment(Qt.AlignCenter)
        copyright_label_line2.setAlignment(Qt.AlignCenter)

        # Set font for the labels
        font = QFont("Arial", 10)
        copyright_label_line1.setFont(font)
        copyright_label_line2.setFont(font)

        # Add the labels to the main layout
        main_layout.addWidget(copyright_label_line1)
        main_layout.addWidget(copyright_label_line2)

        # Initialize RFID monitoring after UI setup
        self.initialize_rfid_monitoring()

    def create_content_layout(self):
        """Creates and returns the main content layout."""
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)  # Increase spacing between elements

        # Create and add the left form layout
        left_form_layout = create_left_form_layout(self.vehicle_info)
        content_layout.addLayout(left_form_layout)

        # Add a vertical separator
        separator1 = self.create_separator()
        content_layout.addWidget(separator1)

        # Create and add the right form layout
        right_form_layout = create_right_form_layout(self.vehicle_info)
        content_layout.addLayout(right_form_layout)

        # Add another vertical separator
        separator2 = self.create_separator()
        content_layout.addWidget(separator2)

        # Create and add the image and clock layout
        image_clock_layout = self.create_image_clock_layout()
        content_layout.addLayout(image_clock_layout)

        return content_layout

    def create_image_clock_layout(self):
        """Creates and returns the image and clock layout."""
        image_clock_layout = QVBoxLayout()
        image_clock_layout.setSpacing(10)  # Add spacing between the image and clock

        clock_frame = create_clock_frame(self)
        image_clock_layout.addWidget(clock_frame, 0, Qt.AlignCenter)

        # Add the image label
        image_label = create_image_label(self)
        image_label.setFixedSize(400, 150)  # Set size for the image
        image_clock_layout.addWidget(image_label, 0, Qt.AlignCenter)

        return image_clock_layout

    def create_separator(self):
        """Creates and returns a vertical separator."""
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #2c3e50;")
        return separator

    def initialize_rfid_monitoring(self):
        """Initialize RFID monitoring."""
        initialize_rfid_monitoring(
            self.vehicle_info['rfidInputLeft'], 
            self.vehicle_info['rfidInputRight'], 
            self.vehicle_info['statusLabel'], 
            self.vehicle_info['indicatorLabel'], 
            self.vehicle_info,
            self  # Pass the window instance for reset functionality
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec_())
