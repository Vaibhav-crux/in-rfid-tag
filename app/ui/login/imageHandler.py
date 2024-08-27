import requests
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt

def fetch_and_process_image(radius):
    """Fetches an image from a predefined URL and processes it into a circular shape."""
    url = "https://wallpapercave.com/uwp/uwp4394072.jpeg"  # URL of the image
    
    # Download the image using requests
    response = requests.get(url)
    
    pixmap = QPixmap()
    pixmap.loadFromData(response.content)
    
    # Create circular mask for the image
    circular_pixmap = QPixmap(pixmap.scaled(2 * radius, 2 * radius, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
    mask = QPixmap(circular_pixmap.size())
    mask.fill(Qt.transparent)
    
    painter = QPainter(mask)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QBrush(Qt.black))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, mask.width(), mask.height())
    painter.end()
    
    circular_pixmap.setMask(mask.mask())
    
    return circular_pixmap
