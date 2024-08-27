# app/ui/mainWindow/mainWindow.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .title_bar import create_title_bar
from .image_label import create_image_label

class FullScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def load_stylesheet(self, file_path):
        """Utility function to load and return a stylesheet."""
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Stylesheet file not found: {file_path}")
            return ""

    def initUI(self):
        # Remove the default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showMaximized()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)  # Set the layout for the window

        # Create custom title bar and add to layout
        title_bar_frame = create_title_bar(self)
        main_layout.addWidget(title_bar_frame)

        # Add the image as the content
        image_label = create_image_label(self)
        main_layout.addWidget(image_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec_())
