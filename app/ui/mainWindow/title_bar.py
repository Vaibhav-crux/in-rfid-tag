from PyQt5.QtWidgets import QFrame, QHBoxLayout
from app.ui.titleBar.window_controls import create_minimize_button, create_close_button, create_image_button
from app.ui.mainWindow.fileScan import open_file_scan_dialog

def create_title_bar(parent):
    title_bar_frame = QFrame(parent)
    title_bar_frame.setFixedHeight(40)
    title_bar_frame.setStyleSheet(parent.load_stylesheet('app/stylesheet/mainWindow/titleBar.qss'))
    title_bar_layout = QHBoxLayout(title_bar_frame)
    title_bar_layout.setContentsMargins(0, 0, 0, 0)

    # Add the image button to the title bar
    image_button = create_image_button(parent)
    image_button.clicked.connect(lambda: open_file_scan_dialog(parent, parent.vehicle_info))  # Pass vehicle_info when opening the dialog
    title_bar_layout.addWidget(image_button)

    # Spacer to push the buttons to the right
    title_bar_layout.addStretch()

    # Add minimize and close buttons to the title bar
    minimize_button = create_minimize_button(parent)
    close_button = create_close_button(parent)
    title_bar_layout.addWidget(minimize_button)
    title_bar_layout.addWidget(close_button)

    return title_bar_frame
