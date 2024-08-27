# app/ui/mainWindow/title_bar.py

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QMenuBar
from app.ui.titleBar.window_controls import create_minimize_button, create_close_button

def create_title_bar(parent):
    title_bar_frame = QFrame(parent)
    title_bar_frame.setFixedHeight(40)
    title_bar_frame.setStyleSheet(parent.load_stylesheet('app/stylesheet/mainWindow/titleBar.qss'))
    title_bar_layout = QHBoxLayout(title_bar_frame)
    title_bar_layout.setContentsMargins(0, 0, 0, 0)
    

    # Spacer to push the buttons to the right
    title_bar_layout.addStretch()

    # Add minimize and close buttons to the title bar
    minimize_button = create_minimize_button(parent)
    close_button = create_close_button(parent)
    title_bar_layout.addWidget(minimize_button)
    title_bar_layout.addWidget(close_button)

    return title_bar_frame
