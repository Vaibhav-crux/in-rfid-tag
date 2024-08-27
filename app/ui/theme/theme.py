import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor

from app.ui.login.login import LoginWindow


def set_dark_mode(app):
    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    app.setPalette(dark_palette)
    app.setStyleSheet("""
        QPushButton {
            background-color: #333333;
            color: white;
            border: 1px solid #555555;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QWidget {
            background-color: #353535;
        }
    """)

def set_light_mode(app):
    light_palette = QPalette()

    light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.Base, QColor(255, 255, 255))
    light_palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.Text, QColor(0, 0, 0))
    light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    light_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    light_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    app.setPalette(light_palette)
    app.setStyleSheet("""
        QPushButton {
            background-color: #f0f0f0;
            color: black;
            border: 1px solid #cccccc;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        QWidget {
            background-color: #f5f5f5;
        }
    """)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Toggle between dark mode and light mode
    mode = 'dark'  # Change to 'light' to use light mode
    if mode == 'dark':
        set_dark_mode(app)
    else:
        set_light_mode(app)

    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
