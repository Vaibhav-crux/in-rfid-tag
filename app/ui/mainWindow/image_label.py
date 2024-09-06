from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

def create_image_label(parent):
    """Creates a QLabel with an image loaded from a predefined file."""

    # Local image file path
    image_path = "app/file/starlab.png"
    
    image_label = QLabel(parent)
    
    # Set fixed size for the image label
    image_label.setFixedSize(400, 200)

    # Load the image from the file
    pixmap = load_image_from_file(image_path)

    if not pixmap.isNull():
        # Scale the image to fit within the fixed size of the label, maintaining aspect ratio
        pixmap = pixmap.scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet(parent.load_stylesheet('app/stylesheet/mainWindow/imageLabel.qss'))
    else:
        image_label.setText("Failed to load image")
        image_label.setAlignment(Qt.AlignCenter)

    return image_label

def load_image_from_file(file_path):
    """Loads an image from a file."""
    try:
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            return pixmap
        else:
            print(f"Failed to load image from {file_path}")
            return QPixmap()
    except Exception as e:
        print(f"An error occurred while loading the image: {e}")
        return QPixmap()
