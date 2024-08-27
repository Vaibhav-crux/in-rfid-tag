# app/ui/mainWindow/image_label.py

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests

def create_image_label(parent):
    """Creates a QLabel with an image loaded from a predefined URL."""
    
    # Predefined image URL
    image_url = "https://wallpapercave.com/wp/wp8313585.jpg"
    
    image_label = QLabel(parent)
    pixmap = load_image_from_url(image_url)

    if not pixmap.isNull():
        # Scale the image to cover the full screen, potentially cropping it
        pixmap = pixmap.scaled(parent.width(), parent.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet(parent.load_stylesheet('app/stylesheet/mainWindow/imageLabel.qss'))
    else:
        image_label.setText("Failed to load image")
        image_label.setAlignment(Qt.AlignCenter)

    return image_label

def load_image_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            return pixmap
        else:
            print(f"Failed to load image. Status code: {response.status_code}")
            return QPixmap()
    except Exception as e:
        print(f"An error occurred while loading the image: {e}")
        return QPixmap()
